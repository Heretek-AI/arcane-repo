#!/usr/bin/env python3
"""
Verification script for S02 (archive stale templates).
Validates archived/active separation, registry validity, non-serviceable tagging,
and audit completeness.

Run: python scripts/verify-s02.py
"""
import json
import os
import subprocess
import sys
import io

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS = "[PASS]"
FAIL = "[FAIL]"
results = []


def check(name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((name, status, detail))
    print(f"  {status} {name}" + (f" — {detail}" if detail else ""))
    return condition


def main():
    print("=" * 60)
    print("S02 Verification Script")
    print("=" * 60)

    # 1. archived/ exists with at least 1 template
    archived_dir = os.path.join(ROOT, "archived")
    archived_exists = os.path.isdir(archived_dir)
    if archived_exists:
        archived_entries = os.listdir(archived_dir)
        # Exclude non-template files
        archived_templates = [
            e for e in archived_entries
            if os.path.isdir(os.path.join(archived_dir, e))
            and not e.startswith(".")
            and e != "__pycache__"
        ]
        archived_count = len(archived_templates)
    else:
        archived_count = 0
    check("archived/ exists", archived_exists)
    check("archived/ has >= 1 template", archived_count >= 1,
          f"found {archived_count} templates")

    # 2. archived/ARCHIVE_MANIFEST.md exists and non-empty
    manifest_path = os.path.join(archived_dir, "ARCHIVE_MANIFEST.md")
    manifest_exists = os.path.isfile(manifest_path)
    if manifest_exists:
        manifest_size = os.path.getsize(manifest_path)
    else:
        manifest_size = 0
    check("archived/ARCHIVE_MANIFEST.md exists", manifest_exists)
    check("ARCHIVE_MANIFEST.md is non-empty", manifest_size > 0,
          f"{manifest_size} bytes")

    # 3. No overlap between archived/ and templates/ directory names
    templates_dir = os.path.join(ROOT, "templates")
    if os.path.isdir(templates_dir):
        active_templates = set(
            e for e in os.listdir(templates_dir)
            if os.path.isdir(os.path.join(templates_dir, e))
            and not e.startswith(".")
            and e != "__pycache__"
        )
    else:
        active_templates = set()

    if archived_exists:
        archived_set = set(archived_templates)
        overlap = archived_set & active_templates
        active_count = len(active_templates)
    else:
        overlap = set()
        active_count = 0

    check("No overlap archived/ vs templates/", len(overlap) == 0,
          f"{len(overlap)} overlaps" if overlap else "clean separation")

    # 4. node scripts/build-registry.js --validate-only exits 0
    try:
        result = subprocess.run(
            ["node", "scripts/build-registry.js", "--validate-only"],
            cwd=ROOT, capture_output=True, text=True, timeout=60
        )
        registry_ok = result.returncode == 0
        registry_detail = result.stdout.strip().split("\n")[-1] if result.stdout else result.stderr.strip().split("\n")[-1]
    except Exception as e:
        registry_ok = False
        registry_detail = str(e)
    check("Registry validation (build-registry.js --validate-only)", registry_ok,
          registry_detail)

    # 5. Active template count < 1143 (some archived)
    check("Active count < 1143", active_count < 1143,
          f"{active_count} active")

    # 6. At least 25 templates have non-serviceable tag
    ns_count = 0
    for t in os.listdir(templates_dir):
        arcane_path = os.path.join(templates_dir, t, "arcane.json")
        try:
            with open(arcane_path) as f:
                d = json.load(f)
            if "non-serviceable" in d.get("tags", []):
                ns_count += 1
        except Exception:
            pass
    check(">= 25 non-serviceable templates", ns_count >= 25,
          f"{ns_count} non-serviceable")

    # 7. audit-report.json has >= 1100 templates
    audit_path = os.path.join(ROOT, "audit-report.json")
    audit_count = 0
    audit_errors = 0
    if os.path.isfile(audit_path):
        with open(audit_path) as f:
            audit_data = json.load(f)
        audit_templates = audit_data.get("templates", [])
        audit_count = len(audit_templates)
        audit_errors = sum(
            1 for t in audit_templates
            if any(f.get("severity") == "error" for f in t.get("findings", []))
        )
    check("audit-report.json >= 1100 templates", audit_count >= 1100,
          f"{audit_count} templates")
    check("Audit errors < 5 (quality baseline)", audit_errors < 5,
          f"{audit_errors} error-level findings")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Archived templates: {archived_count}")
    print(f"  Active templates:   {active_count}")
    print(f"  Total tracked:      {archived_count + active_count}")
    print(f"  Non-serviceable:    {ns_count}")
    print(f"  Audit report:       {audit_count} templates, {audit_errors} errors")
    print(f"  Registry:           validates with {active_count} active")

    passed = sum(1 for _, s, _ in results if s == PASS)
    total = len(results)
    print(f"\n  Checks: {passed}/{total} passed")

    if passed < total:
        print(f"\n{FAIL} — {total - passed} check(s) failed")
        return 1
    else:
        print(f"\n{PASS} — All checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
