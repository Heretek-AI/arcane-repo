#!/usr/bin/env python3
"""
Tests for scripts/remediate-wave.py -- M008 remediation batch generation.

5 assertions as required by the T01 task plan:
1. Correct batch count (ceil(filtered / batch_size))
2. 10 templates per batch (except possibly the last)
3. Prompt includes healthcheck instructions
4. Prompt requires 7+ README sections
5. Derived URLs present where derivable

Dependencies: Python stdlib only (no external packages).
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

# Import the module
import importlib.util

spec = importlib.util.spec_from_file_location(
    "remediate_wave", Path(__file__).parent / "remediate-wave.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _make_fake_audit_report(tmp: Path, template_count: int) -> Path:
    """Create a minimal audit report with template_count templates having doc warnings."""
    templates = []
    for i in range(template_count):
        tid = f"test-template-{i:03d}"
        templates.append({
            "id": tid,
            "name": f"Test Template {i}",
            "tags": ["self-hosted"],
            "issues": [
                {
                    "dimension": "documentation",
                    "severity": "warning",
                    "message": "README contains generic boilerplate text",
                    "suggested_fix": "Replace with project-specific content",
                },
                {
                    "dimension": "compose",
                    "severity": "info",
                    "message": f"Service '{tid}' lacks a healthcheck definition",
                    "suggested_fix": "Add a healthcheck",
                },
            ],
        })
    report = {
        "metadata": {"template_count": template_count, "issue_count": len(templates) * 2},
        "summary": {"by_dimension": {"documentation": template_count}, "by_severity": {"warning": template_count}},
        "templates": templates,
    }
    report_path = tmp / "audit-report.json"
    with open(report_path, "w") as f:
        json.dump(report, f)
    return report_path


def _make_fake_templates(tmp: Path, template_count: int) -> Path:
    """Create minimal template directories with arcane.json and docker-compose.yml."""
    templates_dir = tmp / "templates"
    templates_dir.mkdir()
    for i in range(template_count):
        tid = f"test-template-{i:03d}"
        t_dir = templates_dir / tid
        t_dir.mkdir()

        arcane = {
            "id": tid,
            "name": f"Test Template {i}",
            "description": f"Test description for {tid}",
            "version": "1.0.0",
            "author": "test",
            "tags": ["self-hosted"],
        }
        with open(t_dir / "arcane.json", "w") as f:
            json.dump(arcane, f)

        if i % 3 == 0:
            compose = (
                f"version: '3.8'\n\n"
                f"services:\n"
                f"  {tid}:\n"
                f"    image: docker.io/redislabs/redis:latest\n"
                f"    container_name: {tid}\n"
                f"    ports:\n"
                f'      - "${{{tid.upper()}_PORT:-6379}}:6379"\n'
                f"    volumes:\n"
                f"      - {tid}_data:/data\n"
                f"    restart: unless-stopped\n\n"
                f"volumes:\n"
                f"  {tid}_data:\n"
                f"    name: {tid}_data\n"
            )
        elif i % 3 == 1:
            compose = (
                f"version: '3.8'\n\n"
                f"services:\n"
                f"  {tid}:\n"
                f"    image: docker.io/postgres:16\n"
                f"    container_name: {tid}\n"
                f"    ports:\n"
                f'      - "${{{tid.upper()}_PORT:-5432}}:5432"\n'
                f"    environment:\n"
                f"      POSTGRES_USER: app\n"
                f"      POSTGRES_PASSWORD: secret\n"
                f"    volumes:\n"
                f"      - {tid}_data:/var/lib/postgresql/data\n\n"
                f"volumes:\n"
                f"  {tid}_data:\n"
                f"    name: {tid}_data\n"
            )
        else:
            compose = (
                f"version: '3.8'\n\n"
                f"services:\n"
                f"  {tid}:\n"
                f"    image: docker.io/{tid.replace('-', '/')}/{tid}:latest\n"
                f"    container_name: {tid}\n"
                f"    ports:\n"
                f'      - "${{{tid.upper()}_PORT:-8080}}:8080"\n'
                f"    volumes:\n"
                f"      - {tid}_data:/data\n"
                f"    restart: unless-stopped\n\n"
                f"volumes:\n"
                f"  {tid}_data:\n"
                f"    name: {tid}_data\n"
            )
        with open(t_dir / "docker-compose.yml", "w") as f:
            f.write(compose)

    return templates_dir


def test_correct_batch_count():
    """Assertion 1: Batch count matches ceil(filtered / batch_size)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        report_path = _make_fake_audit_report(tmp, 25)
        templates_dir = _make_fake_templates(tmp, 25)

        filtered = mod.load_and_filter_templates(report_path)
        batches = mod.generate_batches(filtered, templates_dir, batch_size=10, wave=1)

        expected = 3
        actual = len(batches)
        assert actual == expected, f"Expected {expected} batches, got {actual}"

    print("[PASS] Assertion 1: Correct batch count")


def test_templates_per_batch():
    """Assertion 2: Each batch has at most batch_size templates (last may be smaller)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        report_path = _make_fake_audit_report(tmp, 25)
        templates_dir = _make_fake_templates(tmp, 25)

        filtered = mod.load_and_filter_templates(report_path)
        batches = mod.generate_batches(filtered, templates_dir, batch_size=10, wave=1)

        for batch in batches:
            count = batch["template_count"]
            assert count <= 10, f"Batch {batch['batch_id']} has {count} templates (max 10)"

        assert batches[-1]["template_count"] == 5, \
            f"Last batch should have 5, got {batches[-1]['template_count']}"

    print("[PASS] Assertion 2: Correct templates per batch")


def test_prompt_includes_healthcheck():
    """Assertion 3: Subagent prompt includes specific healthcheck patterns."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        report_path = _make_fake_audit_report(tmp, 3)
        templates_dir = _make_fake_templates(tmp, 3)

        filtered = mod.load_and_filter_templates(report_path)
        batches = mod.generate_batches(filtered, templates_dir, batch_size=10, wave=1)

        for batch in batches:
            for t in batch["templates"]:
                prompt = t["subagent_prompt"]
                assert "wget" in prompt, f"Prompt for {t['id']} missing wget healthcheck"
                assert "redis-cli" in prompt, f"Prompt for {t['id']} missing redis-cli healthcheck"
                assert "pg_isready" in prompt, f"Prompt for {t['id']} missing pg_isready healthcheck"

    print("[PASS] Assertion 3: Prompt includes healthcheck instructions")


def test_prompt_requires_readme_sections():
    """Assertion 4: Subagent prompt requires 7+ README sections."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        report_path = _make_fake_audit_report(tmp, 3)
        templates_dir = _make_fake_templates(tmp, 3)

        filtered = mod.load_and_filter_templates(report_path)
        batches = mod.generate_batches(filtered, templates_dir, batch_size=10, wave=1)

        required_sections = mod.REQUIRED_README_SECTIONS
        assert len(required_sections) >= 7, f"Only {len(required_sections)} sections defined"

        for batch in batches:
            for t in batch["templates"]:
                prompt = t["subagent_prompt"]
                for section in required_sections:
                    assert section in prompt, \
                        f"Prompt for {t['id']} missing README section: {section}"

    print("[PASS] Assertion 4: Prompt requires 7+ README sections")


def test_derived_urls_present():
    """Assertion 5: Derived URLs present where derivable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        report_path = _make_fake_audit_report(tmp, 6)
        templates_dir = _make_fake_templates(tmp, 6)

        filtered = mod.load_and_filter_templates(report_path)
        batches = mod.generate_batches(filtered, templates_dir, batch_size=10, wave=1)

        derived_count = 0
        for batch in batches:
            for t in batch["templates"]:
                url = t.get("derived_project_url")
                if url:
                    derived_count += 1
                    assert url.startswith("https://github.com/"), \
                        f"Derived URL for {t['id']} is not GitHub: {url}"

        assert derived_count > 0, "No derived project URLs found across any template"

    print(f"[PASS] Assertion 5: Derived URLs present ({derived_count} templates with URLs)")


def main() -> None:
    print("Running remediate-wave.py tests...\n")
    tests = [
        test_correct_batch_count,
        test_templates_per_batch,
        test_prompt_includes_healthcheck,
        test_prompt_requires_readme_sections,
        test_derived_urls_present,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test_fn.__name__}: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    if failed:
        sys.exit(1)
    print("All tests passed!")


if __name__ == "__main__":
    main()
