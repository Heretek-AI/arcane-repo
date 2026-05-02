#!/usr/bin/env python3
"""
archive-stale.py — Identify and archive stale templates from audit report.

Reads audit-report.json, finds templates with Docker images not updated in >365 days,
and either outputs the list (--dry-run) or moves them to archived/ via git mv.

Usage:
    python scripts/archive-stale.py                  # output stale template list (dry run)
    python scripts/archive-stale.py --execute        # actually move templates to archived/
    python scripts/archive-stale.py --execute --manifest-only  # regenerate manifest only
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STALE_THRESHOLD_DAYS = 365
ROOT_DIR = Path(__file__).resolve().parent.parent
AUDIT_REPORT = ROOT_DIR / "audit-report.json"
TEMPLATES_DIR = ROOT_DIR / "templates"
ARCHIVED_DIR = ROOT_DIR / "archived"
MANIFEST_PATH = ARCHIVED_DIR / "ARCHIVE_MANIFEST.md"


def load_audit_report() -> dict:
    """Load and validate audit-report.json."""
    if not AUDIT_REPORT.exists():
        print(f"ERROR: {AUDIT_REPORT} not found. Run audit-final.py first.", file=sys.stderr)
        sys.exit(1)
    with open(AUDIT_REPORT, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "templates" not in data:
        print("ERROR: audit-report.json missing 'templates' key.", file=sys.stderr)
        sys.exit(1)
    return data


def extract_stale_templates(data: dict) -> list[dict]:
    """Extract templates with freshness warnings where days_since_update > threshold."""
    stale = []
    for t in data["templates"]:
        template_id = t["id"]
        fresh_findings = [f for f in t.get("findings", []) if f["dimension"] == "freshness"]
        if not fresh_findings:
            # No freshness data (non-serviceable / inline base images) — skip
            continue
        for finding in fresh_findings:
            days = finding.get("details", {}).get("days_since_update", 0)
            if days > STALE_THRESHOLD_DAYS:
                stale.append({
                    "id": template_id,
                    "name": t.get("name", template_id),
                    "days_since_update": days,
                    "last_updated": finding["details"].get("last_updated", "unknown"),
                })
                break  # one entry per template
    return sorted(stale, key=lambda x: x["days_since_update"], reverse=True)


def move_templates(stale_list: list[dict]) -> tuple[int, list[str]]:
    """Move stale templates from templates/ to archived/ using git mv."""
    ARCHIVED_DIR.mkdir(exist_ok=True)
    moved = 0
    errors = []
    for entry in stale_list:
        src = TEMPLATES_DIR / entry["id"]
        dst = ARCHIVED_DIR / entry["id"]
        if not src.is_dir():
            errors.append(f"SKIP {entry['id']}: source directory not found")
            continue
        if dst.exists():
            errors.append(f"SKIP {entry['id']}: already exists in archived/")
            continue
        try:
            subprocess.run(
                ["git", "mv", str(src), str(dst)],
                check=True,
                cwd=str(ROOT_DIR),
                capture_output=True,
                text=True,
            )
            moved += 1
        except subprocess.CalledProcessError as e:
            errors.append(f"ERROR {entry['id']}: git mv failed — {e.stderr.strip()}")
    return moved, errors


def write_manifest(stale_list: list[dict], moved_count: int, errors: list[str]) -> None:
    """Write ARCHIVE_MANIFEST.md documenting archived templates."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# Archive Manifest",
        "",
        f"**Date:** {now}",
        f"**Reason:** Docker image not updated in >{STALE_THRESHOLD_DAYS} days (stale)",
        f"**Threshold:** {STALE_THRESHOLD_DAYS} days since last Docker image update",
        f"**Total archived:** {moved_count}",
        "",
        "## Archived Templates",
        "",
        "| Template | Days Stale | Last Updated |",
        "|----------|-----------|--------------|",
    ]
    for entry in stale_list:
        last = entry["last_updated"][:10] if entry["last_updated"] != "unknown" else "unknown"
        lines.append(f"| {entry['id']} | {entry['days_since_update']} | {last} |")
    lines.extend([
        "",
        "## Notes",
        "",
        "- Templates archived here are excluded from the active registry (registry.json).",
        "- To restore a template: `git mv archived/<name> templates/<name>` then rebuild registry.",
        "- Non-serviceable templates (inline base images) without freshness data were not archived.",
    ])
    if errors:
        lines.extend([
            "",
            "## Errors During Archival",
            "",
        ])
        for err in errors:
            lines.append(f"- {err}")
    MANIFEST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Archive stale templates from audit report")
    parser.add_argument("--execute", action="store_true", help="Actually move templates (default: dry-run)")
    parser.add_argument("--manifest-only", action="store_true", help="Regenerate manifest from already-archived templates")
    args = parser.parse_args()

    data = load_audit_report()
    stale_list = extract_stale_templates(data)

    print(f"Found {len(stale_list)} stale templates (>{STALE_THRESHOLD_DAYS} days)")

    if args.manifest_only:
        # Just regenerate manifest from current state
        already_archived = [e for e in stale_list if (ARCHIVED_DIR / e["id"]).is_dir()]
        write_manifest(already_archived, len(already_archived), [])
        print(f"Manifest regenerated for {len(already_archived)} archived templates")
        return

    if not args.execute:
        # Dry run — just print the list
        for entry in stale_list:
            last = entry["last_updated"][:10] if entry["last_updated"] != "unknown" else "unknown"
            print(f"  {entry['id']}: {entry['days_since_update']} days stale (last: {last})")
        print(f"\nRun with --execute to move {len(stale_list)} templates to archived/")
        return

    # Execute mode — move templates
    moved, errors = move_templates(stale_list)
    print(f"Moved {moved} templates to archived/")
    if errors:
        print(f"Encountered {len(errors)} errors:")
        for err in errors:
            print(f"  {err}")

    # Write manifest
    # Only include actually moved templates in manifest
    actually_archived = [e for e in stale_list if (ARCHIVED_DIR / e["id"]).is_dir()]
    write_manifest(actually_archived, len(actually_archived), errors)
    print(f"Manifest written to {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
