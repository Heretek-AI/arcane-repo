#!/usr/bin/env python3
"""
recover-rq.py — Recover review-queue candidates by searching Docker Hub

Reads review-queue.json and searches Docker Hub (v2 search API) for images
that the preflight pipeline missed — candidates whose Docker images exist
under a different maintainer or image name than the three standard heuristics
(library/<name>, <name>/<name>, ghcr.io/<name>/<name>).

For each recoverable candidate, produces a fact card compatible with
process-candidates.py so templates can be created.  Also checks GHCR for
the recovered repo name.

Usage:
    python3 scripts/recover-rq.py --source umbrel
    python3 scripts/recover-rq.py --source portainer --limit 20 --dry-run
    python3 scripts/recover-rq.py --source yunohost --output recovered-fact-cards.json

Then feed to process-candidates.py:
    python3 scripts/process-candidates.py --source umbrel --input recovered-fact-cards.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RQ_PATH = os.path.join(ROOT_DIR, "review-queue.json")
DEFAULT_OUTPUT = os.path.join(ROOT_DIR, "recovered-fact-cards.json")

# ---------------------------------------------------------------------------
# Docker Hub search + web API
# ---------------------------------------------------------------------------

def _http_get_json(url: str, timeout: float = 10.0, max_retries: int = 2) -> tuple[int, dict | list | None]:
    """GET a URL and return (status_code, parsed_json_or_None).

    Retries on 429 (rate limit) and 5xx with exponential backoff.
    """
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, headers={
            "User-Agent": "gsd-recover-rq/1.0",
            "Accept": "application/json",
        })
        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body)
        except urllib.error.HTTPError as e:
            if attempt < max_retries and (e.code == 429 or e.code >= 500):
                retry_after = e.headers.get("Retry-After") or e.headers.get("retry-after")
                delay = float(retry_after) if retry_after else (2.0 * (2 ** attempt))
                time.sleep(delay)
                continue
            return e.code, None
        except Exception:
            if attempt < max_retries:
                time.sleep(2.0 * (2 ** attempt))
                continue
            return 0, None
    return 0, None


def search_docker_hub(name: str, max_results: int = 5) -> list[dict]:
    """Search Docker Hub for images matching `name`.

    Returns results sorted by pull_count descending.
    """
    query = urllib.request.quote(name)
    url = f"https://hub.docker.com/v2/search/repositories/?query={query}&page_size={max_results}"
    status, data = _http_get_json(url)
    if status != 200 or not data:
        return []
    results = data.get("results", [])
    # Sort by pull_count descending
    results.sort(key=lambda r: r.get("pull_count", 0), reverse=True)
    return results


def verify_dh_image(repo_name: str) -> tuple[bool, str | None]:
    """Check Docker Hub web API to confirm a repo exists and is public.

    Returns (exists_public, note).
    """
    url = f"https://hub.docker.com/v2/repositories/{repo_name}/"
    req = urllib.request.Request(url, headers={
        "User-Agent": "gsd-recover-rq/1.0",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        if data.get("is_private", False):
            return False, "private"
        return True, None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "not found"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"network error: {e}"


def get_dh_tags(repo_name: str, limit: int = 20) -> list[str]:
    """Get tags for a Docker Hub image via registry API (Bearer auth)."""
    parts = repo_name.split("/")
    if len(parts) == 1:
        ns, img = "library", parts[0]
    else:
        ns, img = parts[0], "/".join(parts[1:])

    # Step 1: get Bearer token
    token_url = f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{ns}/{img}:pull"
    status, token_data = _http_get_json(token_url)
    if status != 200 or not token_data:
        return []
    token = token_data.get("token", "")

    # Step 2: list tags
    tags_url = f"https://registry-1.docker.io/v2/{ns}/{img}/tags/list"
    req = urllib.request.Request(tags_url, headers={
        "User-Agent": "gsd-recover-rq/1.0",
        "Authorization": f"Bearer {token}",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("tags", [])[:limit]
    except Exception:
        return []


def check_ghcr_image(repo_name: str, limit: int = 20) -> tuple[bool, list[str], str | None]:
    """Check GHCR for an image via Bearer auth.
    
    Returns (reachable, tags_list, note).
    """
    parts = repo_name.split("/")
    if len(parts) < 2:
        return False, [], "invalid ghcr path"
    org, img = parts[0], "/".join(parts[1:])

    # Get token
    token_url = f"https://ghcr.io/token?scope=repository:{org}/{img}:pull"
    status, token_data = _http_get_json(token_url)
    if status != 200 or not token_data:
        return False, [], f"token HTTP {status}"
    token = token_data.get("token", "")

    # List tags
    tags_url = f"https://ghcr.io/v2/{org}/{img}/tags/list"
    req = urllib.request.Request(tags_url, headers={
        "User-Agent": "gsd-recover-rq/1.0",
        "Authorization": f"Bearer {token}",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        tags = data.get("tags", [])[:limit]
        return len(tags) > 0, tags, None
    except urllib.error.HTTPError as e:
        return False, [], f"HTTP {e.code}"
    except Exception as e:
        return False, [], f"network error: {e}"


# ---------------------------------------------------------------------------
# Scoring: pick the best Docker Hub result for a candidate
# ---------------------------------------------------------------------------

def score_result(result: dict, candidate_name: str) -> float:
    """Score a Docker Hub search result for relevance to the candidate.

    Higher = better match.  Returns 0.0 for non-matches (should be discarded).

    Factors:
      - Must have substring overlap between candidate and image name
      - pull_count (log scale) is a tiebreaker, not a primary signal
      - Exact image name match scores highest
      - Penalize 'library/' namespace
    """
    repo = result.get("repo_name", "")
    if "/" in repo:
        ns, img = repo.split("/", 1)
    else:
        ns, img = "library", repo

    candidate_lower = candidate_name.lower().strip()
    img_lower = img.lower().strip()

    # Must have substring overlap — reject unrelated results
    if candidate_lower not in img_lower and img_lower not in candidate_lower:
        return 0.0

    score = 0.0

    # Name match (primary signal)
    if img_lower == candidate_lower:
        score += 20.0  # exact match
    elif candidate_lower in img_lower:
        # Closer match = better; penalize length difference
        len_ratio = len(candidate_lower) / max(len(img_lower), 1)
        score += 8.0 * len_ratio
    elif img_lower in candidate_lower:
        len_ratio = len(img_lower) / max(len(candidate_lower), 1)
        score += 5.0 * len_ratio

    # Pull count as tiebreaker (log scale)
    pulls = result.get("pull_count", 0)
    if pulls > 0:
        import math
        score += min(math.log10(pulls), 10.0) * 0.5

    # Penalize library namespace
    if ns == "library":
        score -= 3.0

    return score


def find_best_image(candidate_name: str, max_search_results: int = 10) -> tuple[str | None, str | None, float | None]:
    """Search Docker Hub for `candidate_name` and return the best matching repo.

    Returns (repo_name_or_None, reason_str, score_or_None).
    """
    results = search_docker_hub(candidate_name, max_results=max_search_results)
    if not results:
        return None, "no search results", None

    # Score and sort — reject 0-score results (no substring overlap)
    scored = [(r, score_result(r, candidate_name)) for r in results]
    scored = [(r, s) for r, s in scored if s > 0.0]
    scored.sort(key=lambda x: x[1], reverse=True)

    if not scored:
        return None, "no relevant search results (name mismatch)", None

    # Try top candidates in order until we find a public one
    for rank, (result, score) in enumerate(scored[:3]):
        repo = result.get("repo_name", "")
        if not repo:
            continue
        exists, note = verify_dh_image(repo)
        if exists:
            return repo, f"rank {rank + 1}, {result.get('pull_count', 0):,} pulls", score
        # If it's 'not found', that's fine to skip; other errors we note
        if note and note not in ("not found",):
            continue

    return None, f"top {min(3, len(scored))} results not public", None


# ---------------------------------------------------------------------------
# Fact card builder
# ---------------------------------------------------------------------------

def build_fact_card(candidate_name: str, source: str, dh_repo: str,
                    ghcr_repo: str | None, github_url: str | None = None) -> dict:
    """Build a fact card compatible with process-candidates.py."""
    images_checked = []

    # Docker Hub entry
    dh_exists, _dh_note = verify_dh_image(dh_repo)
    dh_img = f"docker.io/{dh_repo}:latest"
    if dh_exists:
        tags = get_dh_tags(dh_repo)
        images_checked.append({
            "registry": "dockerhub",
            "image": dh_img,
            "reachable": True,
            "tags": tags,
            "note": None,
        })
    else:
        images_checked.append({
            "registry": "dockerhub",
            "image": dh_img,
            "reachable": False,
            "tags": [],
            "note": "not found",
        })

    # GHCR entry
    ghcr_img = f"ghcr.io/{dh_repo}:latest"
    ghcr_reachable, ghcr_tags, ghcr_note = check_ghcr_image(dh_repo)
    images_checked.append({
        "registry": "ghcr",
        "image": ghcr_img,
        "reachable": ghcr_reachable,
        "tags": ghcr_tags,
        "note": ghcr_note,
    })

    # Pick recommend_image: prefer GHCR if reachable, else Docker Hub
    dhs_entry = images_checked[0]
    ghcr_entry = images_checked[1]
    
    if ghcr_entry["reachable"]:
        recommend_image = ghcr_entry["image"]
    elif dhs_entry["reachable"]:
        recommend_image = dhs_entry["image"]
    else:
        recommend_image = None

    return {
        "candidate": candidate_name,
        "source": source,
        "github_url": github_url,
        "images_checked": images_checked,
        "recommend_image": recommend_image,
        "classification_hints": ["docker-ready"] if recommend_image else [],
        "errors": [],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Recover review-queue candidates by searching Docker Hub for alternate image names")
    parser.add_argument("--source", help="Filter to a specific source catalog")
    parser.add_argument("--input", default=DEFAULT_RQ_PATH,
                        help="Path to review-queue.json (default: review-queue.json)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Path for recovered fact cards output")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max candidates to process (default: 0 = all)")
    parser.add_argument("--min-score", type=float, default=0.0,
                        help="Minimum score for a result to be considered (default: 0)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Search but don't write output file")
    parser.add_argument("--verbose", action="store_true", default=True,
                        help="Print per-candidate status")
    args = parser.parse_args()

    # Load review queue
    if not os.path.exists(args.input):
        print(f"ERROR: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        rq = json.load(f)

    # Filter by source if specified
    if args.source:
        rq = [e for e in rq if e.get("source", "").lower() == args.source.lower()]
        if not rq:
            print(f"ERROR: No review-queue entries for source '{args.source}'", file=sys.stderr)
            sys.exit(1)
        print(f"Processing {len(rq)} entries for source '{args.source}'")
    else:
        print(f"Processing {len(rq)} total review-queue entries")

    if args.limit > 0:
        rq = rq[:args.limit]
        print(f"Limited to {args.limit} entries")

    # Process
    recovered = []
    still_missing = []
    start_time = time.time()

    # Load parsed candidates for github_url cross-referencing
    github_map = {}
    parsed_path = os.path.join(ROOT_DIR, "candidates-parsed.json")
    if os.path.exists(parsed_path):
        with open(parsed_path, "r", encoding="utf-8") as f:
            for c in json.load(f):
                key = (c.get("name", ""), c.get("source", ""))
                if c.get("github_url"):
                    github_map[key] = c.get("github_url")

    for i, entry in enumerate(rq):
        name = entry.get("candidate", "unknown")
        source = entry.get("source", "")

        # Search
        best_repo, reason, best_score = find_best_image(name)

        if best_repo is None or best_score is None:
            if args.verbose:
                print(f"[{i + 1}/{len(rq)}] MISSING  {name} ({source}): {reason}")
            still_missing.append(entry)
            continue

        # Apply minimum score threshold if set
        if args.min_score > 0 and best_score < args.min_score:
            if args.verbose:
                print(f"[{i + 1}/{len(rq)}] LOWSCORE {name} ({source}): {best_repo} score={best_score:.1f} — {reason}")
            still_missing.append(entry)
            continue

        if args.verbose:
            print(f"[{i + 1}/{len(rq)}] RECOVERED {name} ({source}): {best_repo} score={best_score:.1f} — {reason}")

        # Cross-reference github_url from parsed candidates
        gh_url = github_map.get((name, source))
        fc = build_fact_card(name, source, best_repo, None, gh_url)
        recovered.append((entry, fc))

        # Rate-limit friendly pause (0.6–1.0s with jitter)
        time.sleep(0.6 + (time.time() % 0.4))

    elapsed = time.time() - start_time

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Recovery complete in {elapsed:.1f}s")
    print(f"  Total processed: {len(rq)}")
    print(f"  Recovered: {len(recovered)} ({len(recovered)*100//len(rq) if rq else 0}%)")
    print(f"  Still missing: {len(still_missing)} ({len(still_missing)*100//len(rq) if rq else 0}%)")

    if recovered:
        fact_cards = [fc for _entry, fc in recovered]
        if not args.dry_run:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(fact_cards, f, indent=2)
                f.write("\n")
            print(f"  Wrote {len(fact_cards)} fact cards to {args.output}")

            # Print next steps
            source_flag = f"--source {args.source} " if args.source else ""
            print(f"\nNext: python3 scripts/process-candidates.py {source_flag}--input {os.path.basename(args.output)}")
        else:
            print(f"  [DRY-RUN] Would write {len(fact_cards)} fact cards to {args.output}")
            # Show sample
            for entry, fc in recovered[:3]:
                print(f"\n  Sample: {fc['candidate']} -> {fc['recommend_image']}")

    # Show a few still-missing by source
    if still_missing:
        print(f"\nStill-missing by source:")
        by_src = {}
        for e in still_missing:
            s = e.get("source", "unknown")
            by_src[s] = by_src.get(s, 0) + 1
        for s, c in sorted(by_src.items(), key=lambda x: x[1], reverse=True):
            print(f"  {s}: {c}")


if __name__ == "__main__":
    main()
