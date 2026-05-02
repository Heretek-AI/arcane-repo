#!/usr/bin/env python3
"""
Fix audit findings: tag non-serviceable templates.

Scans all ``templates/*/docker-compose.yml`` for bare base-language image
refs (``python:X-slim``, ``node:X-alpine``, ``php:X-fpm-alpine``) that
indicate placeholder/FastAPI templates, then adds the ``non-serviceable``
tag to the corresponding ``arcane.json`` if not already present.

Only adds the tag — does NOT modify image refs or any other metadata.

Usage:
    python scripts/fix-audit-findings.py [--dry-run] [--templates-dir DIR]

Exit codes:
    0  success (at least one template modified or dry-run)
    1  fatal error
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

logger = logging.getLogger("fix-audit")
logger.setLevel(logging.INFO)

# Patterns that indicate inline base images (non-serviceable placeholders)
# Matches: python:3.12-slim, python:3.11-slim, node:20-alpine, node:18-alpine,
#          php:8.3-fpm-alpine, etc.
INLINE_BASE_RE = re.compile(
    r"^image:\s+(?P<ref>"
    r"python:\d[\d.]*-slim"
    r"|node:\d[\d.]*-alpine"
    r"|php:\d[\d.]*-fpm-alpine"
    r")\s*$"
)


def find_non_serviceable_templates(templates_dir: Path) -> list[str]:
    """Return template IDs whose docker-compose.yml uses inline base images."""
    results: list[str] = []

    for template_dir in sorted(templates_dir.iterdir()):
        if not template_dir.is_dir():
            continue

        compose_path = template_dir / "docker-compose.yml"
        if not compose_path.exists():
            continue

        try:
            text = compose_path.read_text("utf-8", errors="replace")
        except OSError as e:
            logger.warning("Cannot read %s: %s", compose_path, e)
            continue

        for line in text.splitlines():
            if INLINE_BASE_RE.match(line.strip()):
                results.append(template_dir.name)
                break  # One match per template is enough

    return results


def tag_template(arcane_path: Path, dry_run: bool = False) -> bool:
    """Add 'non-serviceable' tag to arcane.json if not present.

    Returns True if the tag was added (or would be added in dry-run).
    Returns False if already present or on error.
    """
    try:
        with open(arcane_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error("Cannot parse %s: %s", arcane_path, e)
        return False
    except OSError as e:
        logger.error("Cannot read %s: %s", arcane_path, e)
        return False

    tags: list[str] = data.get("tags", [])
    if "non-serviceable" in tags:
        return False  # Already tagged

    tags.append("non-serviceable")
    data["tags"] = tags

    if not dry_run:
        try:
            with open(arcane_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        except OSError as e:
            logger.error("Cannot write %s: %s", arcane_path, e)
            return False

    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tag non-serviceable templates in arcane.json",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be changed without writing files",
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

    templates_dir = Path(args.templates_dir)
    if not templates_dir.is_dir():
        logger.error("Templates directory not found: %s", templates_dir)
        sys.exit(1)

    # Step 1: Find templates with inline base images
    candidates = find_non_serviceable_templates(templates_dir)
    logger.info(
        "Found %d templates with inline base images in docker-compose.yml",
        len(candidates),
    )

    # Step 2: Tag each one
    modified = 0
    already_tagged = 0
    errors = 0

    for tid in candidates:
        arcane_path = templates_dir / tid / "arcane.json"
        if not arcane_path.exists():
            logger.warning("Skipping %s: no arcane.json", tid)
            errors += 1
            continue

        result = tag_template(arcane_path, dry_run=args.dry_run)
        if result:
            modified += 1
            action = "Would tag" if args.dry_run else "Tagged"
            logger.info("%s %s as non-serviceable", action, tid)
        else:
            already_tagged += 1

    # Summary
    logger.info("=" * 60)
    logger.info("Summary:")
    logger.info("  Templates with inline base images: %d", len(candidates))
    logger.info("  Newly tagged non-serviceable:      %d", modified)
    logger.info("  Already tagged:                    %d", already_tagged)
    logger.info("  Errors/skipped:                    %d", errors)
    if args.dry_run:
        logger.info("  (dry-run — no files were modified)")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
