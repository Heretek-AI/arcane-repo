"""
Parse CANDIDATES.md into a structured candidate list with image name mappings.

Reads the markdown file section-by-section and extracts structured data per candidate:
name, source, github_url, yunohost_app, probable_docker_images.

All image-name heuristics are source-specific and produce a list of Docker image
references the pre-flight verifier (T02) will check against Docker Hub v2 and
GHCR APIs.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Optional


# ---------------------------------------------------------------------------
# Section detection
# ---------------------------------------------------------------------------

SECTION_PATTERNS = [
    (re.compile(r"^## Priority Candidates"), "priority"),
    (re.compile(r"^### YunoHost"), "yunohost"),
    (re.compile(r"^### Portainer"), "portainer"),
    (re.compile(r"^### Umbrel"), "umbrel"),
    (re.compile(r"^### awesome-selfhosted"), "awesome-selfhosted"),
    (re.compile(r"^### M012"), "m012"),
    (re.compile(r"^### GitHub"), "priority"),  # treat GitHub section same as priority
]

# Matches a numbered entry:  "1. **Name** ..." or "1.**Name**..."
ENTRY_RE = re.compile(r"^\s*(\d+)[.)]\s*\*{2}(.+?)\*{2}")

# Matches an italic URL: *https://...*
ITALIC_URL_RE = re.compile(r"\*?(https?://[^\s*]+)\*?")

# Matches a GitHub URL with owner/repo extraction
GITHUB_REPO_RE = re.compile(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/|#|\?|$)")

# Matches YunoHost app URL
YUNOHOST_APP_RE = re.compile(r"apps\.yunohost\.org/app/([^/\s]+)")

# Matches Umbrel app URL
UMBREL_APP_RE = re.compile(r"github\.com/getumbrel/umbrel-apps/tree/master/([^/\s]+)")

# Matches explicit image reference: | image: xxx (used by portainer)
EXPLICIT_IMAGE_RE = re.compile(r"\|\s*image:\s*(\S+)")
# Matches M012 explicit image reference: Image: `ref`
M012_IMAGE_RE = re.compile(r"[Ii]mage:\s*`([^`]+)`")

# Matches Source Code markdown link: [Source Code](https://github.com/...)
SOURCE_CODE_RE = re.compile(r"\[Source Code\]\((https?://[^)]+)\)")

# Matches Codeberg URL (alternative to GitHub)
CODEBERG_REPO_RE = re.compile(r"codeberg\.org/([^/]+)/([^/]+?)(?:/|#|\?|$)")

# Matches GitLab URL
GITLAB_REPO_RE = re.compile(r"gitlab\.com/([^/]+)/([^/]+?)(?:/|#|\?|$)")


# ---------------------------------------------------------------------------
# Helper: sanitise candidate name to a reasonable image-name token
# ---------------------------------------------------------------------------

def _name_to_token(name: str) -> str:
    """Normalise a human-readable name into a lowercase, hyphen-safe token."""
    return re.sub(r"[^a-z0-9_-]", "", name.lower().replace(" ", "-").replace("&", "-"))


# ---------------------------------------------------------------------------
# Image-name generators per source
# ---------------------------------------------------------------------------

def _yunohost_images(name: str, app_name: Optional[str], github_url: Optional[str]) -> list[str]:
    """Generate probable Docker image names for YunoHost candidates."""
    token = app_name or _name_to_token(name)
    images = [
        f"docker.io/library/{token}:latest",
        f"docker.io/{token}/{token}:latest",
        f"ghcr.io/{token}/{token}:latest",
    ]
    if github_url:
        repo_images = _github_images(github_url)
        for img in repo_images:
            if img not in images:
                images.append(img)
    return images


def _portainer_images(name: str, raw_description: str, github_url: Optional[str]) -> list[str]:
    """Generate probable Docker image names for Portainer candidates."""
    # Check for explicit image ref first
    explicit = EXPLICIT_IMAGE_RE.search(raw_description)
    if explicit:
        image_ref = explicit.group(1)
        # If it already has a tag, include it as-is; add a latest variant
        if ":" in image_ref:
            return [image_ref]
        return [f"{image_ref}:latest"]

    token = _name_to_token(name)
    images = [
        f"docker.io/{token}/{token}:latest",
        f"docker.io/library/{token}:latest",
        f"ghcr.io/{token}/{token}:latest",
    ]
    if github_url:
        repo_images = _github_images(github_url)
        for img in repo_images:
            if img not in images:
                images.append(img)
    return images


def _umbrel_images(name: str, app_name: Optional[str], github_url: Optional[str]) -> list[str]:
    """Generate probable Docker image names for Umbrel candidates."""
    token = app_name or _name_to_token(name)
    images = [
        f"docker.io/{token}/{token}:latest",
        f"docker.io/library/{token}:latest",
        f"ghcr.io/{token}/{token}:latest",
    ]
    if github_url:
        repo_images = _github_images(github_url)
        for img in repo_images:
            if img not in images:
                images.append(img)
    return images


def _awesome_selfhosted_images(name: str, github_url: Optional[str]) -> list[str]:
    """Generate probable Docker image names for awesome-selfhosted candidates."""
    if github_url:
        images = _github_images(github_url)
        # Also add docker.io variants for GitHub repos
        m = GITHUB_REPO_RE.search(github_url)
        if m:
            owner, repo = m.group(1).lower(), m.group(2).lower()
            hub_img = f"docker.io/{owner}/{repo}:latest"
            if hub_img not in images:
                images.append(hub_img)
        if images:
            return images
        # If github_url was present but couldn't be parsed (truncated),
        # fall through to name-based heuristics
    token = _name_to_token(name)
    return [
        f"docker.io/{token}/{token}:latest",
        f"ghcr.io/{token}/{token}:latest",
    ]


def _priority_images(github_url: Optional[str]) -> list[str]:
    """Generate probable Docker image names for Priority/GitHub candidates."""
    if not github_url:
        return []
    return _github_images(github_url)


def _m012_images(name: str, raw_description: str, github_url: Optional[str]) -> list[str]:
    """Generate probable Docker image names for M012 candidates.

    M012 entries have explicit Image: `ref` metadata, which is the primary source.
    Fallback to GitHub-derived images.
    """
    # Check for explicit image ref first (Image: `ref`)
    explicit = M012_IMAGE_RE.search(raw_description)
    if explicit:
        image_ref = explicit.group(1)
        if ":" in image_ref:
            return [image_ref]
        return [f"{image_ref}:latest"]

    # Fallback: derive from GitHub URL
    if github_url:
        return _github_images(github_url)

    return []


def _github_images(github_url: str) -> list[str]:
    """Generate Docker image refs from a GitHub repository URL."""
    m = GITHUB_REPO_RE.search(github_url)
    if not m:
        return []
    owner = m.group(1).lower()
    repo = m.group(2).lower()
    return [
        f"ghcr.io/{owner}/{repo}:latest",
        f"docker.io/{owner}/{repo}:latest",
    ]


# ---------------------------------------------------------------------------
# Core: parse CANDIDATES.md lines → list of candidate dicts
# ---------------------------------------------------------------------------

def _extract_entry_lines(lines: list[str], start_idx: int) -> tuple[list[str], int]:
    """Collect all lines belonging to the entry starting at start_idx."""
    entry_lines: list[str] = []
    i = start_idx + 1
    while i < len(lines):
        line = lines[i]
        # Stop at next numbered entry or next section header
        stripped = line.strip()
        if ENTRY_RE.match(line) or (stripped.startswith("## ") or stripped.startswith("### ")):
            break
        entry_lines.append(line)
        i += 1
    return entry_lines, i


def _extract_github_from_urls(text: str, *, exclude_umbrel_catalog: bool = False) -> Optional[str]:
    """Return the first GitHub URL found in text blocks.

    When exclude_umbrel_catalog is True, skips URLs containing getumbrel/umbrel-apps.
    """
    # Check Source Code links
    sc_matches = SOURCE_CODE_RE.findall(text)
    for url in sc_matches:
        if GITHUB_REPO_RE.search(url):
            if exclude_umbrel_catalog and "getumbrel/umbrel-apps" in url:
                continue
            return url
    # Check italic URLs
    url_matches = ITALIC_URL_RE.findall(text)
    for url in url_matches:
        if GITHUB_REPO_RE.search(url):
            if exclude_umbrel_catalog and "getumbrel/umbrel-apps" in url:
                continue
            return url
    return None


def _extract_any_github_url(text: str) -> Optional[str]:
    """Extract any GitHub URL from text (used as fallback)."""
    # Raw URL scan
    for match in re.finditer(r"https?://github\.com/[^\s)\]]+", text):
        return match.group(0).rstrip(")").rstrip("]").rstrip(".")
    return None


def parse_candidates(filepath: str) -> list[dict]:
    """Parse CANDIDATES.md and return a list of structured candidate dicts.

    Each dict has:
      - name (str)
      - source (str): one of priority, yunohost, portainer, umbrel, awesome-selfhosted
      - github_url (str | None)
      - yunohost_app (str | None)
      - stars (int | None)
      - probable_images (list[str])
    """
    with open(filepath, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    candidates: list[dict] = []
    current_source = "unknown"
    entry_starts: list[tuple[int, str]] = []  # (line_idx, source)

    # Pass 1: detect section boundaries and entry positions
    for idx, line in enumerate(lines):
        for pattern, source in SECTION_PATTERNS:
            if pattern.search(line):
                current_source = source
                break
        if ENTRY_RE.match(line):
            entry_starts.append((idx, current_source))

    # Pass 2: parse each entry
    for start_idx, source in entry_starts:
        header_line = lines[start_idx]
        m = ENTRY_RE.match(header_line)
        if not m:
            continue
        name = m.group(2).strip()

        # Collect continuation lines; header_line is included for text scans
        entry_continuation, _ = _extract_entry_lines(lines, start_idx)
        all_text = header_line + " " + " ".join(entry_continuation)
        continuation_text = " ".join(entry_continuation)

        # --- Extract GitHub URL ---
        github_url: Optional[str] = None

        if source == "priority":
            # Priority entries have *https://github.com/...* on the next line
            for el in entry_continuation:
                url_match = ITALIC_URL_RE.search(el)
                if url_match and GITHUB_REPO_RE.search(url_match.group(1)):
                    github_url = url_match.group(1).rstrip("*").rstrip(")")
                    break
            if not github_url:
                github_url = _extract_any_github_url(all_text)

        elif source == "yunohost":
            # YunoHost entries may have a GitHub URL in the description (some variants)
            github_url = _extract_github_from_urls(all_text)

        elif source == "portainer":
            # Portainer: check for Source Code links or explicit image refs with ghcr.io
            github_url = _extract_github_from_urls(all_text)

        elif source == "umbrel":
            # Umbrel: exclude the umbrel-apps catalog URL itself
            github_url = _extract_github_from_urls(all_text, exclude_umbrel_catalog=True)

        elif source == "awesome-selfhosted":
            # awesome-selfhosted: [Source Code](https://github.com/...)
            github_url = _extract_github_from_urls(all_text)
            if not github_url:
                github_url = _extract_any_github_url(all_text)

        elif source == "m012":
            # M012 entries have *https://github.com/...* on the next line
            for el in entry_continuation:
                url_match = ITALIC_URL_RE.search(el)
                if url_match and GITHUB_REPO_RE.search(url_match.group(1)):
                    github_url = url_match.group(1).rstrip("*").rstrip(")")
                    break
            if not github_url:
                github_url = _extract_any_github_url(all_text)

        # --- Extract YunoHost app name ---
        yunohost_app: Optional[str] = None
        if source == "yunohost":
            for el in entry_continuation:
                ym = YUNOHOST_APP_RE.search(el)
                if ym:
                    yunohost_app = ym.group(1)
                    break

        # --- Extract Umbrel app name ---
        umbrel_app: Optional[str] = None
        if source == "umbrel":
            for el in entry_continuation:
                um = UMBREL_APP_RE.search(el)
                if um:
                    umbrel_app = um.group(1)
                    break

        # --- Extract stars (priority only) ---
        stars: Optional[int] = None
        if source == "priority":
            star_match = re.search(r"([\d,]+)\s*★", header_line)
            if star_match:
                stars = int(star_match.group(1).replace(",", ""))

        # --- Generate image names ---
        if source == "priority":
            images = _priority_images(github_url)
        elif source == "yunohost":
            images = _yunohost_images(name, yunohost_app, github_url)
        elif source == "portainer":
            images = _portainer_images(name, all_text, github_url)
        elif source == "umbrel":
            images = _umbrel_images(name, umbrel_app, github_url)
        elif source == "awesome-selfhosted":
            images = _awesome_selfhosted_images(name, github_url)
        elif source == "m012":
            images = _m012_images(name, all_text, github_url)
        else:
            images = []

        candidate = {
            "name": name,
            "source": source,
            "github_url": github_url,
            "yunohost_app": yunohost_app or umbrel_app,
            "stars": stars,
            "probable_images": images,
        }
        candidates.append(candidate)

    return candidates


# ---------------------------------------------------------------------------
# CLI entry-point (writes candidates-parsed.json to cwd)
# ---------------------------------------------------------------------------

def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else "CANDIDATES.md"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "candidates-parsed.json"

    candidates = parse_candidates(input_path)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(candidates, fh, indent=2, ensure_ascii=False)

    # Summary to stderr
    sources = {}
    for c in candidates:
        s = c["source"]
        sources[s] = sources.get(s, 0) + 1

    print(f"Parsed {len(candidates)} candidates from {len(sources)} sources:", file=sys.stderr)
    for src, count in sorted(sources.items()):
        print(f"  {src}: {count}", file=sys.stderr)
    print(f"Wrote {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
