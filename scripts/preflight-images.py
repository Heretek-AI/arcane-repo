#!/usr/bin/env python3
"""
Pre-flight image verification pipeline.

Reads a parsed-candidates JSON (from candidate_parser.py), checks each
Docker image reference against Docker Hub v2 + GHCR APIs, and outputs
fact cards (JSON) with reachability data for downstream subagents.

Usage:
    python scripts/preflight-images.py [--input candidates-parsed.json]
                                       [--output fact-cards.json]
                                       [--limit N]
                                       [--verbose]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure we can import the lib package
# ---------------------------------------------------------------------------
_here = Path(__file__).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

from lib.registry_client import (
    check_dockerhub_image,
    check_ghcr_image,
    get_dockerhub_tags,
    get_stats,
)

logger = logging.getLogger("preflight")
logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Image-ref parser
# ---------------------------------------------------------------------------

# We expect refs of the form:  <registry>/<namespace>/<name>[:<tag>]
# where <registry> is docker.io or ghcr.io
_REF_RE = re.compile(
    r"^(?P<registry>docker\.io|ghcr\.io)/(?P<namespace>[^/]+)/(?P<image>[^:@]+)(?::(?P<tag>.+))?$"
)


def _parse_image_ref(ref: str) -> dict | None:
    """Decompose an image ref into registry, namespace, and image parts.

    Returns ``None`` if the ref cannot be parsed (malformed, unsupported registry).
    """
    m = _REF_RE.match(ref.strip())
    if not m:
        return None
    return {
        "registry": "dockerhub" if m.group("registry") == "docker.io" else "ghcr",
        "namespace": m.group("namespace"),
        "image": m.group("image"),
        "tag": m.group("tag") or "latest",
        "original_ref": ref.strip(),
    }


# ---------------------------------------------------------------------------
# Per-image checking
# ---------------------------------------------------------------------------


def _check_one_image(parsed_ref: dict) -> dict:
    """Check a single image ref and return an ``images_checked`` entry."""
    registry: str = parsed_ref["registry"]
    ns: str = parsed_ref["namespace"]
    img: str = parsed_ref["image"]
    ref: str = parsed_ref["original_ref"]

    if registry == "ghcr":
        result = check_ghcr_image(ns, img)
        return {
            "registry": "ghcr",
            "image": ref,
            "reachable": result["reachable"],
            "tags": result.get("tags", []),
            "note": "" if result["reachable"] else _failure_note(result.get("status_code", 0)),
        }

    # Docker Hub
    # Step 1: exist via web API
    exist = check_dockerhub_image(ns, img)
    if not exist["exists"]:
        note = exist.get("error") or "not found"
        return {
            "registry": "dockerhub",
            "image": ref,
            "reachable": False,
            "tags": [],
            "note": note,
        }

    # Step 2: fetch tags
    tags = get_dockerhub_tags(ns, img)
    return {
        "registry": "dockerhub",
        "image": ref,
        "reachable": True,
        "tags": tags,
        "note": "",
    }


def _failure_note(status_code: int) -> str:
    """Human-readable note for a failed GHCR check."""
    if status_code == 404:
        return "not found"
    elif status_code == 401:
        return "unauthorized (private or internal)"
    elif status_code == 403:
        return "forbidden"
    elif status_code == 429:
        return "rate limited"
    elif status_code >= 500:
        return f"server error ({status_code})"
    elif status_code == 0:
        return "network error"
    else:
        return f"http_{status_code}"


# ---------------------------------------------------------------------------
# Pipeline state
# ---------------------------------------------------------------------------

class PipelineState:
    """Mutable counters for the running pipeline."""

    def __init__(self) -> None:
        self.total: int = 0
        self.processed: int = 0
        self.reachable: int = 0
        self.unreachable: int = 0
        self.errors: int = 0
        self.unchecked: int = 0


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def _determine_recommend_image(
    images_checked: list[dict],
) -> str | None:
    """Pick the recommended image: first reachable, preferring GHCR."""
    ghcr_candidate: str | None = None
    fallback: str | None = None
    for entry in images_checked:
        if entry["reachable"]:
            if entry["registry"] == "ghcr":
                ghcr_candidate = entry["image"]
            if fallback is None:
                fallback = entry["image"]
    return ghcr_candidate or fallback


def _classification_hints(
    images_checked: list[dict],
    candidate_source: str,
) -> list[str]:
    """Derive classification hints from checked images."""
    hints: list[str] = []
    reachable_entries = [e for e in images_checked if e["reachable"]]

    if reachable_entries:
        hints.append("images-found")
        # Check if any image is on GHCR
        if any(e["registry"] == "ghcr" and e["reachable"] for e in images_checked):
            hints.append("ghcr-available")
    else:
        if not images_checked:
            hints.append("no-images")
        else:
            hints.append("needs-investigation")

    # Source-specific hints
    if candidate_source == "yunohost":
        hints.append("yunohost-source")
    elif candidate_source == "portainer":
        hints.append("portainer-source")
    elif candidate_source == "umbrel":
        hints.append("umbrel-source")
    elif candidate_source == "awesome-selfhosted":
        hints.append("awesome-selfhosted-source")

    return hints


def _build_fact_card(
    candidate: dict,
    images_checked: list[dict],
) -> dict:
    """Build a single fact card from candidate metadata and check results."""
    errors: list[str] = []
    for entry in images_checked:
        if not entry["reachable"]:
            errors.append(f"unreachable: {entry['registry']}/{entry['image']} — {entry['note']}")

    if not images_checked and not candidate.get("probable_images"):
        errors.append("no image names inferred")

    return {
        "candidate": candidate["name"],
        "source": candidate["source"],
        "github_url": candidate.get("github_url"),
        "yunohost_url": (
            candidate.get("yunohost_app")
            if candidate.get("source") == "yunohost"
            else None
        ),
        "images_checked": images_checked,
        "recommend_image": _determine_recommend_image(images_checked),
        "classification_hints": _classification_hints(images_checked, candidate["source"]),
        "errors": errors,
    }


def run_pipeline(
    candidates: list[dict],
    *,
    limit: int | None = None,
) -> list[dict]:
    """Run the full preflight pipeline over *candidates*.

    Returns the list of fact cards (one per candidate).
    """
    state = PipelineState()
    state.total = min(len(candidates), limit) if limit else len(candidates)
    fact_cards: list[dict] = []

    for idx, candidate in enumerate(candidates):
        if limit is not None and idx >= limit:
            break

        state.processed += 1
        images_checked: list[dict] = []
        candidate_has_reachable = False

        image_refs: list[str] = candidate.get("probable_images") or []

        if not image_refs:
            # Zero-image candidates still get a fact card
            fact_cards.append(_build_fact_card(candidate, []))
            state.unchecked += 1
            if candidate["source"] != "priority":
                state.unreachable += 1
        else:
            for ref in image_refs:
                parsed = _parse_image_ref(ref)
                if parsed is None:
                    logger.error(
                        "Cannot parse image ref %r for candidate %r",
                        ref,
                        candidate["name"],
                    )
                    images_checked.append({
                        "registry": "unknown",
                        "image": ref,
                        "reachable": False,
                        "tags": [],
                        "note": "malformed_ref",
                    })
                    state.errors += 1
                    continue

                entry = _check_one_image(parsed)
                images_checked.append(entry)

                if entry["reachable"]:
                    candidate_has_reachable = True

            if candidate_has_reachable:
                state.reachable += 1
            else:
                state.unreachable += 1

            fact_cards.append(_build_fact_card(candidate, images_checked))

        # ── Progress reporting (every 10) ──
        if state.processed % 10 == 0 or state.processed == state.total:
            print(
                f"[{state.processed}/{state.total}] checked, "
                f"{state.reachable} reachable, "
                f"{state.unreachable} unreachable, "
                f"{state.errors} errors",
                file=sys.stderr,
            )

    # ── Build summary ──
    stats = get_stats()
    print(
        f"total_candidates={state.total} "
        f"reachable={state.reachable} "
        f"unreachable={state.unreachable} "
        f"rate_limit_hits={stats['rate_limit_hits']} "
        f"network_errors={stats['errors']} "
        f"unchecked={state.unchecked}",
        file=sys.stdout,
    )

    return fact_cards


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pre-flight Docker image verification pipeline",
    )
    parser.add_argument(
        "--input",
        default="candidates-parsed.json",
        help="Path to parsed candidates JSON (default: candidates-parsed.json)",
    )
    parser.add_argument(
        "--output",
        default="fact-cards.json",
        help="Path for fact card output (default: fact-cards.json)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only process first N candidates (default: all)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable DEBUG logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    # ── Load candidates ──
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as fh:
        candidates: list[dict] = json.load(fh)

    logger.info("Loaded %d candidates from %s", len(candidates), args.input)
    print(f"Loaded {len(candidates)} candidates from {args.input}", file=sys.stderr)

    # ── Run pipeline ──
    fact_cards = run_pipeline(candidates, limit=args.limit)

    # ── Write output ──
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(fact_cards, fh, indent=2, ensure_ascii=False)

    print(f"Wrote {len(fact_cards)} fact cards to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
