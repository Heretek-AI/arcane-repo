#!/usr/bin/env python3
"""
Verification script for the preflight-images.py pipeline (M005/S02).

Runs a set of smoke tests against real Docker Hub and GHCR registries to
validate that preflight-images.py correctly verifies image reachability,
handles edge cases, and produces valid output.  Exits 0 only if all
checks pass.

Usage:
    python scripts/verify-preflight.py [--verbose]
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
_PREFLIGHT = _HERE / "preflight-images.py"
_TMP_DIR = _HERE / ".verify-tmp"

PASS = 0
FAIL = 0


def _say(header: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {header}")
    print(f"{'='*60}")


def _check(label: str, condition: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if condition:
        print(f"  PASS  {label}")
        PASS += 1
        return True
    else:
        print(f"  FAIL  {label}  --  {detail}" if detail else f"  FAIL  {label}")
        FAIL += 1
        return False


def _run_preflight(input_path: str, output_path: str, **kwargs: Any) -> subprocess.CompletedProcess:
    """Run preflight-images.py with the given args; return CompletedProcess."""
    cmd = [
        sys.executable,
        str(_PREFLIGHT),
        "--input", str(input_path),
        "--output", str(output_path),
    ]
    if kwargs.get("limit"):
        cmd.extend(["--limit", str(kwargs["limit"])])
    if kwargs.get("verbose"):
        cmd.append("--verbose")

    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _write_json(path: str, data: Any) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Check 1: Script exists and has --help
# ---------------------------------------------------------------------------

def check_01_help() -> None:
    _say("Check 1: Script exists and --help prints usage")

    _check("preflight-images.py exists", _PREFLIGHT.is_file(),
           f"expected at {_PREFLIGHT}")

    cp = subprocess.run(
        [sys.executable, str(_PREFLIGHT), "--help"],
        capture_output=True, text=True, timeout=10,
    )
    _check("--help exits 0", cp.returncode == 0,
           f"exit code = {cp.returncode}")
    _check("--help mentions --input", "--input" in (cp.stdout + cp.stderr))
    _check("--help mentions --output", "--output" in (cp.stdout + cp.stderr))
    _check("--help mentions --limit", "--limit" in (cp.stdout + cp.stderr))
    _check("--help mentions --verbose", "--verbose" in (cp.stdout + cp.stderr))


# ---------------------------------------------------------------------------
# Prepare test candidates
# ---------------------------------------------------------------------------

def _build_test_candidates() -> list[dict]:
    """Return a small candidate list for smoke testing."""
    return [
        {
            "name": "nginx",
            "source": "docker-hub-smoke",
            "github_url": "https://github.com/nginx/nginx",
            "probable_images": [
                "docker.io/library/nginx:latest",
            ],
        },
        {
            "name": "homepage",
            "source": "ghcr-smoke",
            "github_url": "https://github.com/gethomepage/homepage",
            "probable_images": [
                "ghcr.io/gethomepage/homepage:latest",
            ],
        },
        {
            "name": "definitely-not-real",
            "source": "fake-smoke",
            "github_url": None,
            "probable_images": [
                "docker.io/definitelynotreal12345/fakeimage:latest",
                "ghcr.io/definitelynotreal12345/fakeimage:latest",
            ],
        },
        {
            "name": "zero-images-edge",
            "source": "edge-case",
            "github_url": None,
            "probable_images": [],
        },
    ]


# ---------------------------------------------------------------------------
# Check 2: Known-reachable image (Docker Hub — nginx)
# ---------------------------------------------------------------------------

def check_02_dockerhub_reachable(fact_cards: list[dict]) -> None:
    _say("Check 2: Known-reachable Docker Hub image (library/nginx)")

    nginx = next((c for c in fact_cards if c["candidate"] == "nginx"), None)
    _check("nginx candidate exists", nginx is not None)

    if nginx is None:
        return

    images = nginx["images_checked"]
    _check("has at least one image checked", len(images) > 0)

    entry = images[0] if images else {}
    _check("reachable == true", entry.get("reachable") is True,
           f"got: {entry.get('reachable')}")
    _check("tags is non-empty", isinstance(entry.get("tags"), list) and len(entry.get("tags", [])) > 0,
           f"tags: {entry.get('tags')}")
    _check("tags contains 'latest'", "latest" in (entry.get("tags") or []),
           f"tags: {entry.get('tags')}")
    _check("recommend_image is not null", nginx.get("recommend_image") is not None,
           f"recommend_image: {nginx.get('recommend_image')}")


# ---------------------------------------------------------------------------
# Check 3: Known-reachable image (GHCR — gethomepage/homepage)
# ---------------------------------------------------------------------------

def check_03_ghcr_reachable(fact_cards: list[dict]) -> None:
    _say("Check 3: Known-reachable GHCR image (gethomepage/homepage)")

    homepage = next((c for c in fact_cards if c["candidate"] == "homepage"), None)
    _check("homepage candidate exists", homepage is not None)

    if homepage is None:
        return

    images = homepage["images_checked"]
    ghcr_entries = [e for e in images if e.get("registry") == "ghcr"]
    _check("has GHCR entry", len(ghcr_entries) > 0)

    if ghcr_entries:
        entry = ghcr_entries[0]
        _check("GHCR reachable == true", entry.get("reachable") is True,
               f"got: {entry.get('reachable')}, status: {entry.get('note')}")
        _check("GHCR tags populated", isinstance(entry.get("tags"), list) and len(entry.get("tags", [])) > 0,
               f"tags: {entry.get('tags')}")


# ---------------------------------------------------------------------------
# Check 4: Non-existent image returns reachable=false
# ---------------------------------------------------------------------------

def check_04_nonexistent(fact_cards: list[dict]) -> None:
    _say("Check 4: Non-existent image returns reachable=false")

    fake = next((c for c in fact_cards if c["candidate"] == "definitely-not-real"), None)
    _check("fake candidate exists", fake is not None)

    if fake is None:
        return

    images = fake["images_checked"]
    _check("has at least one image checked", len(images) > 0)

    all_unreachable = all(not e.get("reachable", True) for e in images)
    _check("all images_checked[].reachable are false", all_unreachable,
           f"images: {json.dumps(images, indent=2)}")

    _check("recommend_image is null", fake.get("recommend_image") is None,
           f"recommend_image: {fake.get('recommend_image')}")

    # The errors field should contain entries for unreachable images
    errors = fake.get("errors") or []
    _check("has error entries for unreachable images", len(errors) > 0 or len(images) == 0,
           f"errors: {errors}")


# ---------------------------------------------------------------------------
# Check 5: 401-vs-404 distinction (MEM023) — web API used
# ---------------------------------------------------------------------------

def check_05_web_api_distinction(fact_cards: list[dict]) -> None:
    _say("Check 5: 401-vs-404 distinction — Docker Hub web API used")

    # The fake Docker Hub image should produce an images_checked entry
    # that indicates the image doesn't exist — NOT a 401/unauthorized.
    # This confirms the web API path (hub.docker.com/v2/repositories/)
    # was used, not the registry API.

    fake = next((c for c in fact_cards if c["candidate"] == "definitely-not-real"), None)
    _check("fake candidate available for web-API check", fake is not None)

    if fake is None:
        return

    dh_entries = [e for e in fake["images_checked"] if e.get("registry") == "dockerhub"]
    _check("has Docker Hub entry in fake candidate", len(dh_entries) > 0)

    if dh_entries:
        dh_entry = dh_entries[0]
        note = dh_entry.get("note", "")
        # If the web API was used, a non-existent repo should get "not found"
        # (404 from web API). If the registry API was mistakenly used, it would
        # return 401/unauthorized.
        is_not_found = note == "not found"
        _check(
            "non-existent Docker Hub repo maps to 'not found' (web API 404), not 401",
            is_not_found,
            f"note: '{note}' — if 'unauthorized', registry API was used instead of web API",
        )

        # Also verify reachable is false
        _check("Docker Hub entry reachable == false", dh_entry.get("reachable") is False)


# ---------------------------------------------------------------------------
# Check 6: Output file integrity
# ---------------------------------------------------------------------------

def check_06_output_integrity(output_path: str) -> dict | None:
    _say("Check 6: Output file integrity")

    path = Path(output_path)
    _check("fact-cards.json exists", path.is_file(),
           f"expected at {path}")

    if not path.is_file():
        return None

    try:
        fact_cards = _read_json(str(path))
        _check("is valid JSON", True)
    except (json.JSONDecodeError, OSError) as e:
        _check("is valid JSON", False, str(e))
        return None

    _check("is a non-empty array", isinstance(fact_cards, list) and len(fact_cards) > 0,
           f"type: {type(fact_cards).__name__}, len: {len(fact_cards) if isinstance(fact_cards, list) else 'N/A'}")

    REQUIRED = {"candidate", "source", "images_checked", "recommend_image", "errors"}
    all_ok = True
    for idx, card in enumerate(fact_cards):
        missing = REQUIRED - set(card.keys())
        if missing:
            _check(f"entry [{idx}] has all required fields",
                   False, f"missing: {missing}")
            all_ok = False

    if all_ok:
        _check("every entry has all required fields", True)

    # Additional schema checks per entry
    for idx, card in enumerate(fact_cards):
        images = card.get("images_checked")
        if images is not None and isinstance(images, list):
            for j, img in enumerate(images):
                img_req = {"registry", "image", "reachable", "tags", "note"}
                img_missing = img_req - set(img.keys())
                if img_missing:
                    _check(f"entry [{idx}] images_checked[{j}] has required fields",
                           False, f"missing: {img_missing}")

    return fact_cards if all_ok else None


# ---------------------------------------------------------------------------
# Check 7: Error handling — network timeout resilience (documented)
# ---------------------------------------------------------------------------

def check_07_timeout_documentation() -> None:
    _say("Check 7: Network timeout resilience (documented check)")

    # We cannot easily simulate a network timeout, but we can verify that:
    # 1. The retry logic exists in registry_client.py
    # 2. The pipeline does not crash on errors (already confirmed by check 4)

    client_src = _HERE / "lib" / "registry_client.py"
    _check("registry_client.py exists", client_src.is_file())

    if client_src.is_file():
        src = client_src.read_text(encoding="utf-8")
        _check("retry_with_backoff function exists", "_retry_with_backoff" in src)
        _check("catches URLError / TimeoutError",
               "URLError" in src and "TimeoutError" in src)

    # Document expected behavior
    print()
    print("  Expected timeout behavior:")
    print("     - On network timeout: _retry_with_backoff retries N times")
    print("     - After retries exhausted: returns status=0, logs error to stderr")
    print("     - Pipeline marks image as unreachable with note='network error'")
    print("     - Pipeline continues to next candidate (non-fatal)")
    print("     - Network errors counted in summary stats")


# ---------------------------------------------------------------------------
# Check 8: Zero-image edge case
# ---------------------------------------------------------------------------

def check_08_zero_images(fact_cards: list[dict]) -> None:
    _say("Check 8: Zero-image candidate edge case")

    zero = next((c for c in fact_cards if c["candidate"] == "zero-images-edge"), None)
    _check("zero-image candidate exists", zero is not None)

    if zero is None:
        return

    images = zero["images_checked"]
    _check("images_checked is empty array", isinstance(images, list) and len(images) == 0,
           f"images: {images}")

    _check("recommend_image is null", zero.get("recommend_image") is None)

    errors = zero.get("errors") or []
    has_no_images_error = any("no image names inferred" in str(e) for e in errors)
    _check("errors contains 'no image names inferred'", has_no_images_error,
           f"errors: {errors}")

    hints = zero.get("classification_hints") or []
    has_no_images_hint = "no-images" in hints
    _check("classification_hints contains 'no-images'", has_no_images_hint,
           f"hints: {hints}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    global PASS, FAIL

    print("preflight-images.py — Verification Suite")
    print(f"Project root: {_PROJECT_ROOT}")
    print(f"Preflight:    {_PREFLIGHT}")
    print()

    # Ensure the tmp directory is clean
    _TMP_DIR.mkdir(parents=True, exist_ok=True)

    # ── Check 1: Help ──
    check_01_help()

    # ── Prepare test candidates ──
    candidates_path = str(_TMP_DIR / "test-candidates.json")
    _write_json(candidates_path, _build_test_candidates())

    # ── Run the pipeline ──
    output_path = str(_TMP_DIR / "fact-cards.json")
    print(f"\n  Running preflight-images.py against test candidates...")
    t0 = time.monotonic()
    cp = _run_preflight(candidates_path, output_path)
    elapsed = time.monotonic() - t0

    print(f"  Preflight completed in {elapsed:.1f}s, exit code {cp.returncode}")
    if cp.stderr:
        # Show stderr lines (progress logs)
        for line in cp.stderr.strip().splitlines():
            print(f"  [stderr] {line}")
    if cp.stdout:
        print(f"  [stdout] {cp.stdout.strip()}")

    _check("preflight exits 0", cp.returncode == 0,
           f"exit code = {cp.returncode}, stderr tail: {cp.stderr[-200:] if cp.stderr else 'none'}")

    # ── Load fact cards ──
    fact_cards = _read_json(output_path) if Path(output_path).is_file() else []
    _check("fact-cards.json was produced", len(fact_cards) > 0)

    if not fact_cards:
        print("\n  ❌ No fact cards produced — stopping early.")
        sys.exit(1)

    # ── Run remaining checks ──
    check_02_dockerhub_reachable(fact_cards)
    check_03_ghcr_reachable(fact_cards)
    check_04_nonexistent(fact_cards)
    check_05_web_api_distinction(fact_cards)

    # Check 6 returns fact_cards if schema is valid (or None)
    validated = check_06_output_integrity(output_path)
    if validated is None:
        fact_cards_from_recheck = _read_json(output_path) if Path(output_path).is_file() else []
    else:
        fact_cards_from_recheck = validated

    check_07_timeout_documentation()
    check_08_zero_images(fact_cards_from_recheck or fact_cards)

    # ── Final summary ──
    _say("Summary")
    total = PASS + FAIL
    print(f"  Checks: {total} total, {PASS} passed, {FAIL} failed")
    print()

    if FAIL == 0:
        print("  All verification checks passed.")
        sys.exit(0)
    else:
        print(f"  {FAIL} check(s) failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
