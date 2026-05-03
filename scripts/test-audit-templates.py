#!/usr/bin/env python3
"""
Integration tests for scripts/audit-templates.py.

Creates temporary template fixtures with known quality issues, runs the
audit script against them, and asserts expected findings are produced.

Each test covers one audit dimension:
  - compose_healthcheck:  Service missing healthcheck → detected
  - compose_restart:      Service missing restart policy → detected
  - compose_valid:        Clean compose with healthcheck + restart → pass
  - boilerplate_readme:   README with generic boilerplate → detected
  - provenance:           Description with 'sourced from' marker → detected
  - metadata_missing:     arcane.json missing required fields → detected
  - metadata_placeholder: Description is placeholder text → detected
  - clean_template:       Template with no issues → empty issues list
  - non_serviceable:      Skipped (zero issues)

Usage:
    python scripts/test-audit-templates.py

Dependencies: Python stdlib only.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Fixture definitions
# ---------------------------------------------------------------------------

# Base arcane.json that satisfies all required fields
BASE_ARCANE_JSON: dict = {
    "id": "test",
    "name": "Test Template",
    "description": "A real test template for validation",
    "version": "1.0.0",
    "author": "Arcane",
    "tags": ["self-hosted"],
}

# Base compose with healthcheck and restart — the "clean" baseline
# Uses library/nginx (generic image) so provenance doesn't derive a project URL
BASE_COMPOSE_YML: str = """\
version: "3.8"
services:
  web:
    image: library/nginx:latest
    ports:
      - "8080:80"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
"""

# Base README with real content (not boilerplate)
BASE_README_MD: str = """\
# My App

A self-hosted application for task management.

## Quick Start

1. Copy `.env.example` to `.env`
2. Run `docker compose up -d`

## Configuration

See the [documentation](https://github.com/myorg/myapp) for details.
"""


def _write_template(
    tmpdir: Path,
    template_id: str,
    arcane: dict | None = None,
    compose: str | None = None,
    readme: str | None = None,
) -> Path:
    """Write a template fixture to disk."""
    tdir = tmpdir / template_id
    tdir.mkdir(parents=True, exist_ok=True)

    if arcane is not None:
        (tdir / "arcane.json").write_text(
            json.dumps(arcane, indent=2), encoding="utf-8"
        )
    if compose is not None:
        (tdir / "docker-compose.yml").write_text(compose, encoding="utf-8")
    if readme is not None:
        (tdir / "README.md").write_text(readme, encoding="utf-8")

    return tdir


def _run_audit(tmpdir: Path) -> dict:
    """Run the audit script against tmpdir and return the parsed JSON report."""
    json_out = tmpdir / "audit-report.json"
    script = Path(__file__).resolve().parent / "audit-templates.py"

    result = subprocess.run(
        [
            sys.executable, str(script),
            "--templates-dir", str(tmpdir),
            "--output-json", str(json_out),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        print(f"=== stdout ===\n{result.stdout}")
        print(f"=== stderr ===\n{result.stderr}")
        raise AssertionError(
            f"audit-templates.py exited with code {result.returncode}"
        )

    assert json_out.exists(), "JSON report not written"
    with open(json_out, encoding="utf-8") as f:
        return json.load(f)


def _find_template(report: dict, template_id: str) -> dict | None:
    """Find a template entry by ID in the report."""
    for t in report["templates"]:
        if t["id"] == template_id:
            return t
    return None


def _has_issue(issues: list[dict], dimension: str, severity: str | None = None, message_contains: str | None = None) -> bool:
    """Check if any issue matches the given criteria."""
    for i in issues:
        if i["dimension"] != dimension:
            continue
        if severity and i["severity"] != severity:
            continue
        if message_contains and message_contains.lower() not in i["message"].lower():
            continue
        return True
    return False


# ---------------------------------------------------------------------------
# Test functions
# ---------------------------------------------------------------------------

def test_compose_healthcheck_detected() -> None:
    """Missing healthcheck is detected for each service."""
    with tempfile.TemporaryDirectory(prefix="test-healthcheck-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Compose WITHOUT healthcheck
        compose_no_hc = """\
version: "3.8"
services:
  app:
    image: myorg/app:latest
    ports:
      - "8080:8080"
    restart: unless-stopped
"""
        _write_template(tmpdir, "no-healthcheck", BASE_ARCANE_JSON, compose_no_hc, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "no-healthcheck")
        assert t is not None, "Template 'no-healthcheck' not in report"
        assert _has_issue(t["issues"], "compose", severity="info",
                          message_contains="healthcheck"), \
            f"Expected healthcheck issue, got: {t['issues']}"
        print("  PASS: compose_healthcheck_detected")


def test_compose_restart_detected() -> None:
    """Missing restart policy is detected for each service."""
    with tempfile.TemporaryDirectory(prefix="test-restart-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Compose WITHOUT restart policy
        compose_no_restart = """\
version: "3.8"
services:
  app:
    image: myorg/app:latest
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
"""
        _write_template(tmpdir, "no-restart", BASE_ARCANE_JSON, compose_no_restart, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "no-restart")
        assert t is not None, "Template 'no-restart' not in report"
        assert _has_issue(t["issues"], "compose", severity="info",
                          message_contains="restart"), \
            f"Expected restart issue, got: {t['issues']}"
        print("  PASS: compose_restart_detected")


def test_compose_valid_clean() -> None:
    """Clean compose with healthcheck + restart produces no compose issues."""
    with tempfile.TemporaryDirectory(prefix="test-clean-compose-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        _write_template(tmpdir, "clean-compose", BASE_ARCANE_JSON, BASE_COMPOSE_YML, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "clean-compose")
        assert t is not None
        compose_issues = [i for i in t["issues"] if i["dimension"] == "compose"]
        assert len(compose_issues) == 0, \
            f"Expected no compose issues, got: {compose_issues}"
        print("  PASS: compose_valid_clean")


def test_boilerplate_readme_detected() -> None:
    """Boilerplate README patterns are detected."""
    with tempfile.TemporaryDirectory(prefix="test-boilerplate-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        boilerplate_readme = """\
# Activepieces -- Self-Hosted Application

Activepieces is a self-hosted application available through the Portainer catalog.

## Quick Start

1. Copy `.env.example` to `.env`
2. Run `docker compose up -d`
"""
        _write_template(tmpdir, "boilerplate", BASE_ARCANE_JSON, BASE_COMPOSE_YML, boilerplate_readme)

        report = _run_audit(tmpdir)
        t = _find_template(report, "boilerplate")
        assert t is not None
        assert _has_issue(t["issues"], "documentation", severity="warning",
                          message_contains="boilerplate"), \
            f"Expected boilerplate issue, got: {t['issues']}"
        print("  PASS: boilerplate_readme_detected")


def test_provenance_sourced_from() -> None:
    """'sourced from' marker in description is detected."""
    with tempfile.TemporaryDirectory(prefix="test-provenance-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        arcane = dict(BASE_ARCANE_JSON)
        arcane["description"] = "Self-hosted deployment via Docker, sourced from Yunohost catalog"

        _write_template(tmpdir, "provenance", arcane, BASE_COMPOSE_YML, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "provenance")
        assert t is not None
        assert _has_issue(t["issues"], "provenance", severity="info",
                          message_contains="sourced from"), \
            f"Expected 'sourced from' issue, got: {t['issues']}"
        print("  PASS: provenance_sourced_from")


def test_metadata_missing_fields() -> None:
    """Missing required fields in arcane.json are detected."""
    with tempfile.TemporaryDirectory(prefix="test-metadata-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Missing name, version, author
        arcane = {"id": "incomplete", "description": "Missing fields", "tags": ["self-hosted"]}
        _write_template(tmpdir, "metadata-missing", arcane, BASE_COMPOSE_YML, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "metadata-missing")
        assert t is not None
        assert _has_issue(t["issues"], "metadata", severity="error",
                          message_contains="Missing required fields"), \
            f"Expected missing fields issue, got: {t['issues']}"
        print("  PASS: metadata_missing_fields")


def test_metadata_placeholder_description() -> None:
    """Placeholder descriptions are detected."""
    with tempfile.TemporaryDirectory(prefix="test-placeholder-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        arcane = dict(BASE_ARCANE_JSON)
        arcane["description"] = "TODO"
        _write_template(tmpdir, "placeholder-desc", arcane, BASE_COMPOSE_YML, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "placeholder-desc")
        assert t is not None
        assert _has_issue(t["issues"], "metadata", severity="warning",
                          message_contains="placeholder"), \
            f"Expected placeholder issue, got: {t['issues']}"
        print("  PASS: metadata_placeholder_description")


def test_clean_template_zero_issues() -> None:
    """A well-formed template produces only pass-level issues (no warnings/errors)."""
    with tempfile.TemporaryDirectory(prefix="test-clean-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        _write_template(tmpdir, "perfect", BASE_ARCANE_JSON, BASE_COMPOSE_YML, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "perfect")
        assert t is not None
        warnings_errors = [i for i in t["issues"] if i["severity"] in ("warning", "error")]
        assert len(warnings_errors) == 0, \
            f"Expected no warnings/errors for clean template, got: {warnings_errors}"
        # Should have at least 1 pass finding for metadata dimension
        pass_findings = [i for i in t["issues"] if i["severity"] == "pass"]
        assert len(pass_findings) >= 1, \
            f"Expected at least 1 pass finding, got: {t['issues']}"
        print("  PASS: clean_template_zero_issues")


def test_non_serviceable_skipped() -> None:
    """Non-serviceable templates are skipped (zero issues)."""
    with tempfile.TemporaryDirectory(prefix="test-nonsvc-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        arcane = dict(BASE_ARCANE_JSON)
        arcane["tags"] = ["non-serviceable", "ai"]
        _write_template(tmpdir, "nonsvc", arcane, BASE_COMPOSE_YML, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "nonsvc")
        assert t is not None
        assert len(t["issues"]) == 0, \
            f"Expected zero issues for non-serviceable template, got: {t['issues']}"
        print("  PASS: non_serviceable_skipped")


def test_report_schema() -> None:
    """The report JSON matches the expected schema."""
    with tempfile.TemporaryDirectory(prefix="test-schema-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        _write_template(tmpdir, "schema-test", BASE_ARCANE_JSON, BASE_COMPOSE_YML, BASE_README_MD)

        report = _run_audit(tmpdir)

        # Top-level keys
        assert "metadata" in report, "Missing 'metadata' key"
        assert "summary" in report, "Missing 'summary' key"
        assert "templates" in report, "Missing 'templates' key"

        # Metadata keys
        meta = report["metadata"]
        for key in ("version", "timestamp", "template_count", "issue_count"):
            assert key in meta, f"Missing metadata key: {key}"

        # Summary keys
        summary = report["summary"]
        assert "by_dimension" in summary, "Missing summary.by_dimension"
        assert "by_severity" in summary, "Missing summary.by_severity"

        # Template entry structure
        for t in report["templates"]:
            for key in ("id", "name", "tags", "issues"):
                assert key in t, f"Template missing key: {key}"
            for i in t["issues"]:
                for key in ("dimension", "severity", "message", "suggested_fix"):
                    assert key in i, f"Issue missing key: {key}"

        print("  PASS: report_schema")


def test_missing_readme() -> None:
    """Missing README.md is detected."""
    with tempfile.TemporaryDirectory(prefix="test-noreadme-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Write template without README
        _write_template(tmpdir, "no-readme", BASE_ARCANE_JSON, BASE_COMPOSE_YML, None)

        report = _run_audit(tmpdir)
        t = _find_template(report, "no-readme")
        assert t is not None
        assert _has_issue(t["issues"], "documentation", severity="warning",
                          message_contains="Missing README"), \
            f"Expected missing README issue, got: {t['issues']}"
        print("  PASS: missing_readme")


def test_missing_compose() -> None:
    """Missing docker-compose.yml is detected."""
    with tempfile.TemporaryDirectory(prefix="test-nocompose-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        _write_template(tmpdir, "no-compose", BASE_ARCANE_JSON, None, BASE_README_MD)

        report = _run_audit(tmpdir)
        t = _find_template(report, "no-compose")
        assert t is not None
        assert _has_issue(t["issues"], "compose", severity="error",
                          message_contains="Missing docker-compose"), \
            f"Expected missing compose issue, got: {t['issues']}"
        print("  PASS: missing_compose")


def test_missing_arcane_json() -> None:
    """Missing arcane.json is detected as a metadata error."""
    with tempfile.TemporaryDirectory(prefix="test-noarcane-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Write compose + readme but no arcane.json
        tdir = tmpdir / "no-arcane"
        tdir.mkdir(parents=True)
        (tdir / "docker-compose.yml").write_text(BASE_COMPOSE_YML, encoding="utf-8")
        (tdir / "README.md").write_text(BASE_README_MD, encoding="utf-8")

        report = _run_audit(tmpdir)
        t = _find_template(report, "no-arcane")
        assert t is not None
        assert _has_issue(t["issues"], "metadata", severity="error",
                          message_contains="Missing arcane.json"), \
            f"Expected missing arcane.json issue, got: {t['issues']}"
        print("  PASS: missing_arcane_json")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("Running audit-templates.py tests...\n")

    tests = [
        test_compose_healthcheck_detected,
        test_compose_restart_detected,
        test_compose_valid_clean,
        test_boilerplate_readme_detected,
        test_provenance_sourced_from,
        test_metadata_missing_fields,
        test_metadata_placeholder_description,
        test_clean_template_zero_issues,
        test_non_serviceable_skipped,
        test_report_schema,
        test_missing_readme,
        test_missing_compose,
        test_missing_arcane_json,
    ]

    passed = 0
    failed = 0

    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR: {test_fn.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")

    if failed:
        print("FAILED")
        return 1

    print("ALL TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
