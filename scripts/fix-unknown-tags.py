#!/usr/bin/env python3
"""
Fix unknown tags in arcane.json files based on audit findings.

Reads ``audit-report.json`` and removes any tags flagged as unknown
(not in the curated KNOWN_TAGS taxonomy) from each template's
``arcane.json``.  Preserves all known tags.

Usage:
    python scripts/fix-unknown-tags.py [--dry-run] [--audit-report PATH]

Exit codes:
    0  success
    1  fatal error
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger("fix-tags")
logger.setLevel(logging.INFO)

# Must match KNOWN_TAGS in audit-final.py
KNOWN_TAGS: set[str] = {
    # source
    "self-hosted", "yunohost", "portainer", "umbrel", "awesome-selfhosted",
    # category
    "ai", "devops", "agents", "communication", "llm", "storage", "rag",
    "monitoring", "framework", "security", "cms", "automation", "search",
    "observability", "database", "tools", "orchestration", "analytics",
    "workflow", "chat", "web", "research", "python", "proxy", "paas",
    "low-code", "inference", "gateway", "sql", "platform", "api", "reference",
    # status
    "multi-service", "non-serviceable", "priority",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fix unknown tags in arcane.json from audit findings",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be changed without writing files",
    )
    parser.add_argument(
        "--audit-report",
        default="audit-report.json",
        help="Path to audit report JSON (default: audit-report.json)",
    )
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Path to templates directory (default: templates)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    report_path = Path(args.audit_report)
    if not report_path.exists():
        logger.error("Audit report not found: %s", report_path)
        sys.exit(1)

    try:
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error("Cannot parse audit report: %s", e)
        sys.exit(1)

    templates_dir = Path(args.templates_dir)

    # Extract unknown-tag warnings from audit
    templates_with_unknown: dict[str, list[str]] = {}
    for t in report.get("templates", []):
        tid = t["id"]
        for f in t.get("findings", []):
            if f["dimension"] == "tags" and f["severity"] == "warning":
                details = f.get("details", {})
                unknown = details.get("unknown_tags", [])
                if unknown:
                    templates_with_unknown[tid] = unknown

    logger.info(
        "Found %d templates with unknown tags in audit report",
        len(templates_with_unknown),
    )

    # Fix each template
    modified = 0
    skipped = 0
    errors = 0
    total_tags_removed = 0

    for tid, unknown_tags in sorted(templates_with_unknown.items()):
        arcane_path = templates_dir / tid / "arcane.json"
        if not arcane_path.exists():
            logger.warning("Skipping %s: no arcane.json", tid)
            errors += 1
            continue

        try:
            with open(arcane_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error("Cannot parse %s: %s", arcane_path, e)
            errors += 1
            continue

        tags: list[str] = data.get("tags", [])
        new_tags = [t for t in tags if t not in unknown_tags or t in KNOWN_TAGS]
        removed = [t for t in tags if t in unknown_tags and t not in KNOWN_TAGS]

        if not removed:
            skipped += 1
            continue

        total_tags_removed += len(removed)
        data["tags"] = new_tags

        if not args.dry_run:
            try:
                with open(arcane_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.write("\n")
            except OSError as e:
                logger.error("Cannot write %s: %s", arcane_path, e)
                errors += 1
                continue

        modified += 1
        action = "Would fix" if args.dry_run else "Fixed"
        logger.info(
            "%s %s: removed %s (kept %s)",
            action, tid, removed, new_tags,
        )

    # Summary
    logger.info("=" * 60)
    logger.info("Summary:")
    logger.info("  Templates with unknown tags: %d", len(templates_with_unknown))
    logger.info("  Templates modified:          %d", modified)
    logger.info("  Tags removed:                %d", total_tags_removed)
    logger.info("  Skipped (already clean):     %d", skipped)
    logger.info("  Errors:                      %d", errors)
    if args.dry_run:
        logger.info("  (dry-run — no files were modified)")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
