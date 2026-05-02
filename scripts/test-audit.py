#!/usr/bin/env python3
"""
Lightweight integration test for audit-final.py.

Creates a temporary template fixture with known-good arcane.json +
docker-compose.yml, runs audit-final.py against it, and asserts expected
findings are produced. Cleans up the fixture on exit.

Usage:
    python scripts/test-audit.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Fixture: a minimal template with known properties
# ---------------------------------------------------------------------------

# A template with 2 services, some stale, some fresh, no errors
FIXTURE_ID = "test-fixture"

FIXTURE_ARCANE_JSON = {
    "id": FIXTURE_ID,
    "name": "Test Fixture",
    # Multiple source tags → triggers classification warning (rule c)
    "tags": ["self-hosted", "portainer", "ai", "monitoring"],
}

FIXTURE_COMPOSE_YML = """\
version: "3.8"
services:
  web:
    image: library/nginx:latest
    ports:
      - "8080:80"

  redis:
    image: library/redis:alpine
    ports:
      - "6379:6379"
"""


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="test-fixture-") as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Write fixture files
        template_dir = tmpdir / FIXTURE_ID
        template_dir.mkdir(parents=True)

        arcane_path = template_dir / "arcane.json"
        with open(arcane_path, "w", encoding="utf-8") as f:
            json.dump(FIXTURE_ARCANE_JSON, f, indent=2)

        compose_path = template_dir / "docker-compose.yml"
        compose_path.write_text(FIXTURE_COMPOSE_YML, encoding="utf-8")

        # Output paths
        json_out = tmpdir / "test-report.json"
        md_out = tmpdir / "test-report.md"

        # Run audit-final.py against fixture
        script_dir = Path(__file__).resolve().parent
        script = script_dir / "audit-final.py"

        result = subprocess.run(
            [
                sys.executable, str(script),
                "--templates-dir", str(tmpdir),
                "--output-json", str(json_out),
                "--output-md", str(md_out),
                "--verbose",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        print("=== stdout ===")
        print(result.stdout)
        if result.stderr:
            print("=== stderr ===")
            print(result.stderr)

        # Check exit code
        assert result.returncode == 0, f"audit-final.py exited with code {result.returncode}"

        # Load JSON report
        assert json_out.exists(), "JSON report not written"
        with open(json_out, encoding="utf-8") as f:
            report = json.load(f)

        # Verify structure
        assert "run_metadata" in report, "Missing run_metadata"
        assert "summary" in report, "Missing summary"
        assert "templates" in report, "Missing templates"
        md = report["run_metadata"]
        assert md["total_templates_scanned"] == 1, f"Expected 1 template, got {md['total_templates_scanned']}"
        assert md["script_version"] == "1.0.0", f"Unexpected script_version: {md['script_version']}"
        assert md["duration_seconds"] > 0, "Duration should be > 0"

        sm = report["summary"]
        assert sm["total_templates"] == 1, f"Expected total_templates=1, got {sm['total_templates']}"
        assert sm["total_findings"] > 0, "Expected at least 1 finding"

        # Verify all 5 dimensions present
        expected_dims = {"reachability", "freshness", "ports", "tags", "classification"}
        dims_present = set(sm["by_dimension"].keys())
        missing_dims = expected_dims - dims_present
        assert not missing_dims, f"Missing dimension(s) in report: {missing_dims}"

        # Verify the test fixture template is in the report
        tmpls = report["templates"]
        fixture_entry = next((t for t in tmpls if t["id"] == FIXTURE_ID), None)
        assert fixture_entry is not None, f"Template '{FIXTURE_ID}' not found in report"
        assert fixture_entry["name"] == "Test Fixture", f"Unexpected name: {fixture_entry['name']}"

        # Verify findings have the correct structure
        for t in tmpls:
            for f in t["findings"]:
                assert "dimension" in f, f"Finding missing 'dimension': {f}"
                assert "severity" in f, f"Finding missing 'severity': {f}"
                assert "message" in f, f"Finding missing 'message': {f}"
                assert f["severity"] in ("pass", "info", "warning", "error"), \
                    f"Unknown severity '{f['severity']}' in: {f}"
                assert f["dimension"] in expected_dims, \
                    f"Unknown dimension '{f['dimension']}' in: {f}"

        # Verify markdown report
        assert md_out.exists(), "Markdown report not written"
        md_text = md_out.read_text(encoding="utf-8")
        assert "# Arcane Template Audit Report" in md_text, "Missing report header"
        assert "## Summary" in md_text, "Missing Summary section"
        assert "## Per-Dimension Findings" in md_text, "Missing Per-Dimension Findings section"

        # Verify each dimension has a section in the markdown
        for dim in expected_dims:
            assert f"### {dim.capitalize()}" in md_text, f"Missing markdown section for {dim}"

        # Verify severity breakdown tables exist
        assert "#### Severity Breakdown" in md_text, "Missing Severity Breakdown subsections"
        assert "#### Per-Template Findings" in md_text, "Missing Per-Template Findings subsections"

        print("\n=== All assertions passed ===")
        return 0


if __name__ == "__main__":
    sys.exit(main())
