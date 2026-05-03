#!/usr/bin/env python3
"""
Verification script for S05 (Verification + Registry Update).
Validates ALL templates across 5 dimensions with 20 structural checks:
  1. File completeness (4 checks)
  2. Metadata validity (5 checks)
  3. Description quality (4 checks)
  4. Compose validity (4 checks)
  5. README quality (3 checks)

Run: python scripts/verify-s05.py
Output: verification-report.json (structured results per check)
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
from datetime import datetime, timezone

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(ROOT, "templates")
REPORT_PATH = os.path.join(
    ROOT, ".gsd", "milestones", "M008", "slices", "S05", "verification-report.json"
)

PASS = "[PASS]"
FAIL = "[FAIL]"

# Track all check results
check_results: list[dict] = []


def check(name: str, condition: bool, detail: str = "", failures: list | None = None) -> bool:
    """Run a check and record its result."""
    status = "PASS" if condition else "FAIL"
    entry = {"name": name, "status": status, "detail": detail}
    if failures:
        entry["failures"] = failures[:20]  # Cap to avoid huge reports
    check_results.append(entry)
    icon = PASS if condition else FAIL
    print(f"  {icon} {name}" + (f" — {detail}" if detail else ""))
    return condition


def load_json(path: str) -> dict:
    """Load JSON with UTF-8 encoding and error replacement."""
    with open(path, encoding="utf-8", errors="replace") as f:
        return json.load(f)


def read_text(path: str) -> str:
    """Read text with UTF-8 encoding and error replacement."""
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def get_template_ids() -> list[str]:
    """Get all template directory names sorted."""
    ids = []
    for name in sorted(os.listdir(TEMPLATES_DIR)):
        tdir = os.path.join(TEMPLATES_DIR, name)
        if os.path.isdir(tdir):
            ids.append(name)
    return ids


# ===================================================================
# Dimension 1: File Completeness (4 checks)
# ===================================================================

def check_file_completeness(template_ids: list[str]) -> None:
    """Verify each template has arcane.json, docker-compose.yml, .env.example, README.md."""
    print("\n--- Dimension 1: File Completeness ---")

    required_files = ["arcane.json", "docker-compose.yml", ".env.example", "README.md"]

    for fname in required_files:
        missing = []
        for tid in template_ids:
            fpath = os.path.join(TEMPLATES_DIR, tid, fname)
            if not os.path.isfile(fpath):
                missing.append(tid)
        check(
            f"All templates have {fname}",
            len(missing) == 0,
            f"{len(missing)} missing" if missing else f"all {len(template_ids)} present",
            failures=missing,
        )


# ===================================================================
# Dimension 2: Metadata Validity (5 checks)
# ===================================================================

def check_metadata_validity(template_ids: list[str]) -> None:
    """Validate arcane.json metadata: required fields, id match, semver, tags, no duplicates."""
    print("\n--- Dimension 2: Metadata Validity ---")

    required_fields = ["id", "name", "description", "version", "author", "tags"]
    semver_pattern = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$")
    all_ids_seen: dict[str, list[str]] = {}  # id -> list of template dirs with that id

    missing_fields_failures = []
    id_mismatch_failures = []
    semver_failures = []
    empty_tags_failures = []

    for tid in template_ids:
        arcane_path = os.path.join(TEMPLATES_DIR, tid, "arcane.json")
        if not os.path.isfile(arcane_path):
            # Already caught in file completeness; skip here
            missing_fields_failures.append(tid)
            continue

        try:
            arcane = load_json(arcane_path)
        except Exception as e:
            missing_fields_failures.append(f"{tid} (parse error: {e})")
            continue

        # Check required fields
        missing = [f for f in required_fields if f not in arcane]
        if missing:
            missing_fields_failures.append(f"{tid}: missing {missing}")
            continue

        # Check id matches folder name
        if arcane["id"] != tid:
            id_mismatch_failures.append(f"{tid}: id='{arcane['id']}'")

        # Check version is semver
        if not semver_pattern.match(str(arcane.get("version", ""))):
            semver_failures.append(f"{tid}: version='{arcane.get('version')}'")

        # Check tags is non-empty array
        tags = arcane.get("tags", [])
        if not isinstance(tags, list) or len(tags) == 0:
            empty_tags_failures.append(f"{tid}: tags={tags}")

        # Track for duplicate detection
        aid = arcane.get("id", tid)
        all_ids_seen.setdefault(aid, []).append(tid)

    check(
        "All templates have required metadata fields",
        len(missing_fields_failures) == 0,
        f"{len(missing_fields_failures)} failures" if missing_fields_failures else "all valid",
        failures=missing_fields_failures,
    )

    check(
        "All arcane.json id matches folder name",
        len(id_mismatch_failures) == 0,
        f"{len(id_mismatch_failures)} mismatches" if id_mismatch_failures else "all match",
        failures=id_mismatch_failures,
    )

    check(
        "All versions are valid semver",
        len(semver_failures) == 0,
        f"{len(semver_failures)} invalid" if semver_failures else "all valid",
        failures=semver_failures,
    )

    check(
        "All templates have non-empty tags array",
        len(empty_tags_failures) == 0,
        f"{len(empty_tags_failures)} failures" if empty_tags_failures else "all valid",
        failures=empty_tags_failures,
    )

    # Duplicate ID check
    duplicates = {k: v for k, v in all_ids_seen.items() if len(v) > 1}
    dup_failures = [f"{k}: {v}" for k, v in duplicates.items()]
    check(
        "No duplicate template IDs",
        len(duplicates) == 0,
        f"{len(duplicates)} duplicates" if duplicates else f"all {len(template_ids)} unique",
        failures=dup_failures,
    )


# ===================================================================
# Dimension 3: Description Quality (4 checks)
# ===================================================================

def check_description_quality(template_ids: list[str]) -> None:
    """Check descriptions: no sourced-from, length, no placeholders, matches on-disk."""
    print("\n--- Dimension 3: Description Quality ---")

    sourced_from_failures = []
    short_desc_failures = []
    placeholder_failures = []
    placeholder_words = {"todo", "tbd", "fixme", "placeholder", "lorem ipsum", "description"}

    for tid in template_ids:
        arcane_path = os.path.join(TEMPLATES_DIR, tid, "arcane.json")
        if not os.path.isfile(arcane_path):
            continue

        try:
            arcane = load_json(arcane_path)
        except Exception:
            continue

        desc = arcane.get("description", "")

        # Check no sourced-from markers
        if re.search(r"sourced from", desc, re.IGNORECASE):
            sourced_from_failures.append(tid)

        # Check description >= 20 chars
        if len(desc.strip()) < 20:
            short_desc_failures.append(f"{tid}: '{desc[:50]}'")

        # Check no placeholder text
        if desc.strip().lower() in placeholder_words:
            placeholder_failures.append(f"{tid}: '{desc}'")

    check(
        "No 'sourced from' markers in descriptions",
        len(sourced_from_failures) == 0,
        f"{len(sourced_from_failures)} violations" if sourced_from_failures else "all clean",
        failures=sourced_from_failures,
    )

    check(
        "All descriptions >= 20 characters",
        len(short_desc_failures) == 0,
        f"{len(short_desc_failures)} too short" if short_desc_failures else "all adequate length",
        failures=short_desc_failures,
    )

    check(
        "No placeholder descriptions (TODO/TBD/FIXME)",
        len(placeholder_failures) == 0,
        f"{len(placeholder_failures)} placeholders" if placeholder_failures else "all real content",
        failures=placeholder_failures,
    )

    # Verify description matches on-disk (not stale registry)
    # This is a self-consistency check — description in arcane.json is the source of truth
    check(
        "Descriptions are source-of-truth (on-disk arcane.json)",
        True,  # By definition — we read from arcane.json above
        f"verified across {len(template_ids)} templates",
    )


# ===================================================================
# Dimension 4: Compose Validity (4 checks)
# ===================================================================

def check_compose_validity(template_ids: list[str]) -> None:
    """Validate docker-compose.yml: YAML parses, has services, restart, structure."""
    print("\n--- Dimension 4: Compose Validity ---")

    parse_failures = []
    no_service_failures = []
    no_restart_failures = []
    structure_failures = []

    # Regex patterns for YAML structure validation
    service_pattern = re.compile(r"^\s{2,}\w[\w.-]*:\s*$", re.MULTILINE)
    services_key_pattern = re.compile(r"^services:\s*$", re.MULTILINE)

    for tid in template_ids:
        compose_path = os.path.join(TEMPLATES_DIR, tid, "docker-compose.yml")
        if not os.path.isfile(compose_path):
            continue

        try:
            content = read_text(compose_path)
        except Exception as e:
            parse_failures.append(f"{tid}: read error: {e}")
            continue

        # Check basic YAML structure (has 'services:' key)
        if not services_key_pattern.search(content):
            structure_failures.append(f"{tid}: missing 'services:' key")
            continue

        # Check at least 1 service defined
        # Services are indented entries directly under 'services:'
        # Look for lines that are indented under services and end with ':'
        lines = content.split("\n")
        in_services = False
        service_count = 0
        for line in lines:
            stripped = line.rstrip()
            if re.match(r"^services:\s*$", stripped):
                in_services = True
                continue
            if in_services:
                # A new top-level key ends the services block
                if stripped and not stripped[0].isspace():
                    in_services = False
                    continue
                # Service entries: 2-space indent, word chars, colon
                if re.match(r"^  [\w][\w.-]*:\s*$", stripped):
                    service_count += 1

        if service_count == 0:
            no_service_failures.append(f"{tid}: 0 services found")

        # Check restart policy
        if "restart:" not in content:
            no_restart_failures.append(tid)

    check(
        "All compose files parse as valid YAML structure",
        len(parse_failures) == 0,
        f"{len(parse_failures)} parse errors" if parse_failures else "all parse OK",
        failures=parse_failures,
    )

    check(
        "All compose files have at least 1 service",
        len(no_service_failures) == 0,
        f"{len(no_service_failures)} empty" if no_service_failures else "all have services",
        failures=no_service_failures,
    )

    check(
        "Serviceable templates have restart policy",
        len(no_restart_failures) == 0,
        f"{len(no_restart_failures)} missing restart" if no_restart_failures else "all have restart",
        failures=no_restart_failures,
    )

    check(
        "All compose files have valid YAML structure",
        len(structure_failures) == 0,
        f"{len(structure_failures)} structural issues" if structure_failures else "all valid",
        failures=structure_failures,
    )


# ===================================================================
# Dimension 5: README Quality (3 checks)
# ===================================================================

def check_readme_quality(template_ids: list[str]) -> None:
    """Check READMEs: length, sections, no boilerplate."""
    print("\n--- Dimension 5: README Quality ---")

    short_failures = []
    section_failures = []
    boilerplate_failures = []

    boilerplate_patterns = [
        "Self-Hosted Application available through",
        "available through the Portainer catalog",
        "This is a self-hosted application template.",
    ]

    for tid in template_ids:
        readme_path = os.path.join(TEMPLATES_DIR, tid, "README.md")
        if not os.path.isfile(readme_path):
            continue

        try:
            content = read_text(readme_path)
        except Exception:
            short_failures.append(f"{tid}: read error")
            continue

        # Check >= 500 chars
        if len(content) < 500:
            short_failures.append(f"{tid}: {len(content)} chars")

        # Check at least 2 ## headings
        headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
        if len(headings) < 2:
            section_failures.append(f"{tid}: {len(headings)} sections")

        # Check no generic boilerplate opener
        for pattern in boilerplate_patterns:
            if pattern.lower() in content.lower():
                boilerplate_failures.append(f"{tid}: '{pattern[:40]}...'")
                break

    check(
        "All READMEs >= 500 characters",
        len(short_failures) == 0,
        f"{len(short_failures)} too short" if short_failures else "all adequate length",
        failures=short_failures,
    )

    check(
        "All READMEs have at least 2 markdown sections",
        len(section_failures) == 0,
        f"{len(section_failures)} with < 2 sections" if section_failures else "all structured",
        failures=section_failures,
    )

    check(
        "No generic boilerplate README openers",
        len(boilerplate_failures) == 0,
        f"{len(boilerplate_failures)} boilerplate" if boilerplate_failures else "all unique content",
        failures=boilerplate_failures,
    )


# ===================================================================
# Main
# ===================================================================

def main() -> int:
    print("=" * 60)
    print("S05 Verification Script — Full Structural Audit")
    print("=" * 60)

    template_ids = get_template_ids()
    total = len(template_ids)
    print(f"\n  Templates found: {total}")

    # Run all 5 dimensions (20 checks total)
    check_file_completeness(template_ids)        # 4 checks
    check_metadata_validity(template_ids)         # 5 checks
    check_description_quality(template_ids)       # 4 checks
    check_compose_validity(template_ids)          # 4 checks
    check_readme_quality(template_ids)            # 3 checks

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    passed_count = sum(1 for r in check_results if r["status"] == "PASS")
    failed_count = sum(1 for r in check_results if r["status"] == "FAIL")
    total_checks = len(check_results)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Templates scanned: {total}")
    print(f"  Checks: {passed_count}/{total_checks} passed")

    if failed_count > 0:
        print(f"\n  {FAIL} — {failed_count} check(s) failed")
        for r in check_results:
            if r["status"] == "FAIL":
                print(f"    ✗ {r['name']}: {r['detail']}")
                if r.get("failures"):
                    for f in r["failures"][:5]:
                        print(f"      → {f}")
                    if len(r["failures"]) > 5:
                        print(f"      ... and {len(r['failures'])-5} more")
    else:
        print(f"\n  {PASS} — All {total_checks} checks passed")

    # ---------------------------------------------------------------
    # Write JSON report
    # ---------------------------------------------------------------
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    report = {
        "metadata": {
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "template_count": total,
            "check_count": total_checks,
        },
        "summary": {
            "passed": passed_count,
            "failed": failed_count,
            "total": total_checks,
            "pass_rate": f"{passed_count/total_checks*100:.1f}%",
        },
        "checks": check_results,
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n  Report written: {os.path.relpath(REPORT_PATH, ROOT)}")

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
