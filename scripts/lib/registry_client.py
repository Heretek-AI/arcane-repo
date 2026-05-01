"""
Docker registry API client layer.

Encapsulates all Docker Hub and GHCR HTTP interactions with auth,
retry, rate-limit detection, and structured logging.  Uses stdlib
only — no external dependencies.

Docker Hub:
  check_dockerhub_image(ns, img)  → web API (distinguishes non-existent vs private)
  get_dockerhub_tags(ns, img)     → registry API with Bearer token

GHCR:
  check_ghcr_image(org, img)      → public tag list (no auth)

Shared:
  get_stats()                     → module-level request / retry / error counters
"""

from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# Module-level stats (inspectable by callers)
# ---------------------------------------------------------------------------
_stats: dict[str, int] = {
    "requests": 0,
    "retries": 0,
    "errors": 0,
    "rate_limit_hits": 0,
}


def get_stats() -> dict[str, int]:
    """Return a copy of the current module-level stats counters."""
    return dict(_stats)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _check_rate_limits(headers: dict[str, str]) -> None:
    """Inspect response headers for rate-limit signals; log & bump stats."""
    remaining_raw = headers.get("X-RateLimit-Remaining") or headers.get(
        "x-ratelimit-remaining"
    )
    if remaining_raw is not None:
        try:
            remaining = int(remaining_raw)
        except ValueError:
            return
        if remaining < 10:
            logger.warning(
                "Rate limit low — X-RateLimit-Remaining=%d", remaining
            )
            _stats["rate_limit_hits"] += 1

    retry_after = headers.get("Retry-After") or headers.get("retry-after")
    if retry_after is not None:
        logger.warning("Rate limit — Retry-After=%s", retry_after)
        _stats["rate_limit_hits"] += 1


def _http_get(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: float = 10.0,
) -> tuple[int, str, dict[str, str]]:
    """Perform a single HTTP GET request via stdlib.

    Returns ``(status_code, body_str, response_headers_dict)``.
    Raises ``urllib.error.HTTPError`` / ``urllib.error.URLError`` on failure —
    callers should wrap this in ``_retry_with_backoff``.
    """
    req_headers: dict[str, str] = dict(headers or {})
    req = urllib.request.Request(url, headers=req_headers)

    logger.debug("HTTP GET %s", url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # type: ignore[attr-defined]
            raw = resp.read()
            body = raw.decode("utf-8", errors="replace")
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            _check_rate_limits(resp_headers)
            _stats["requests"] += 1
            return (resp.status, body, resp_headers)
    except urllib.error.HTTPError as e:
        # Read the error body so downstream code can inspect it.
        error_body = ""
        try:
            error_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        resp_headers = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        _check_rate_limits(resp_headers)
        _stats["requests"] += 1
        raise  # let _retry_with_backoff decide


def _retry_with_backoff(
    fn,
    max_retries: int = 2,
    base_delay: float = 2.0,
) -> tuple[int, str, dict[str, str]]:
    """Call *fn*() with exponential backoff on transient failures.

    *fn* must be a zero-argument callable that returns
    ``(status, body, headers)`` or raises ``HTTPError`` / ``URLError``.

    Transient = HTTP 429, 5xx, or network-level (URLError / OSError / TimeoutError).

    After *max_retries* are exhausted the function returns an error sentinel
    (status=0 for network errors, or the original HTTP status) — it does
    **not** crash.
    """
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            status: int = e.code
            body_str: str = ""
            try:
                body_str = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            err_headers: dict[str, str] = {
                k.lower(): v for k, v in (e.headers.items() if e.headers else [])
            }

            if attempt < max_retries and (status == 429 or status >= 500):
                # Honour Retry-After if present
                retry_raw = err_headers.get("retry-after")
                if retry_raw is not None:
                    try:
                        delay = float(retry_raw)
                    except ValueError:
                        delay = base_delay * (2**attempt)
                else:
                    delay = base_delay * (2**attempt)
                logger.warning(
                    "HTTP %d on attempt %d/%d, retrying in %.1fs",
                    status,
                    attempt + 1,
                    max_retries + 1,
                    delay,
                )
                _stats["retries"] += 1
                time.sleep(delay)
                continue

            # Non-retriable status (4xx except 429) — return immediately
            logger.info("HTTP %d — not retriable, returning result", status)
            _stats["errors"] += 1
            return (status, body_str, err_headers)

        except (urllib.error.URLError, OSError, TimeoutError) as e:
            if attempt < max_retries:
                delay = base_delay * (2**attempt)
                logger.warning(
                    "Network error on attempt %d/%d, retrying in %.1fs: %s",
                    attempt + 1,
                    max_retries + 1,
                    delay,
                    e,
                )
                _stats["retries"] += 1
                time.sleep(delay)
                continue
            logger.error("Network error after %d retries exhausted: %s", max_retries, e)
            _stats["errors"] += 1
            return (0, str(e), {})

    return (0, "max_retries_exceeded", {})


# ---------------------------------------------------------------------------
# Docker Hub — Web API  (distinguishes non-existent vs private)
# ---------------------------------------------------------------------------

def check_dockerhub_image(
    namespace: str,
    image: str,
) -> dict:
    """Check whether a Docker Hub image exists via the **web** API.

    Uses ``GET https://hub.docker.com/v2/repositories/<ns>/<img>/``
    which returns **404** for non-existent repos vs **200** for both
    public and private repos (with ``is_private`` to distinguish).

    Returns
    -------
    dict
        ``exists``, ``is_private``, ``description``, ``stars``,
        ``namespace``, ``image``, ``error`` (None on success).
    """
    url = f"https://hub.docker.com/v2/repositories/{namespace}/{image}/"

    status, body, _headers = _retry_with_backoff(
        lambda: _http_get(url, timeout=10.0)
    )

    base: dict = {
        "namespace": namespace,
        "image": image,
    }

    if status == 404:
        return {**base, "exists": False, "is_private": False, "description": "", "stars": 0, "error": None}
    elif status == 200:
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            logger.error(
                "Malformed JSON from Docker Hub web API for %s/%s — raw: %.200s",
                namespace,
                image,
                body,
            )
            return {**base, "exists": False, "is_private": False, "description": "", "stars": 0, "error": "malformed_response"}
        return {
            **base,
            "exists": True,
            "is_private": bool(data.get("is_private", False)),
            "description": str(data.get("description", "") or ""),
            "stars": int(data.get("star_count", 0) or 0),
            "error": None,
        }
    else:
        # 429, 5xx, network error → treat as unchecked
        return {**base, "exists": False, "is_private": False, "description": "", "stars": 0, "error": f"http_{status}"}


# ---------------------------------------------------------------------------
# Docker Hub — Registry API  (tags, requires Bearer token)
# ---------------------------------------------------------------------------

def get_dockerhub_tags(
    namespace: str,
    image: str,
) -> list[str]:
    """Fetch tag list for a Docker Hub image via the registry API.

    Two-step flow:
    1. Obtain a Bearer token from ``auth.docker.io/token``.
    2. Call ``registry-1.docker.io/v2/<ns>/<img>/tags/list``.

    Returns the tag list (may be empty on failure).
    """
    # ── Step 1: bearer token ────────────────────────────────────────
    token_url = (
        f"https://auth.docker.io/token"
        f"?service=registry.docker.io"
        f"&scope=repository:{namespace}/{image}:pull"
    )

    status, body, _headers = _retry_with_backoff(
        lambda: _http_get(token_url, timeout=10.0)
    )
    if status != 200:
        logger.warning(
            "Failed to obtain auth token for %s/%s — HTTP %d",
            namespace,
            image,
            status,
        )
        return []

    try:
        token_data = json.loads(body)
        token: str = token_data.get("token", "")
    except json.JSONDecodeError:
        logger.error("Malformed token response for %s/%s", namespace, image)
        return []

    if not token:
        logger.warning("Empty token for %s/%s", namespace, image)
        return []

    # ── Step 2: tag list ────────────────────────────────────────────
    tags_url = f"https://registry-1.docker.io/v2/{namespace}/{image}/tags/list"
    status, body, _headers = _retry_with_backoff(
        lambda: _http_get(
            tags_url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
    )
    if status != 200:
        logger.warning(
            "Failed to fetch tags for %s/%s — HTTP %d",
            namespace,
            image,
            status,
        )
        return []

    try:
        data = json.loads(body)
        return data.get("tags", [])
    except json.JSONDecodeError:
        logger.error("Malformed tags response for %s/%s", namespace, image)
        return []


# ---------------------------------------------------------------------------
# GHCR — public tag list (no auth)
# ---------------------------------------------------------------------------

def check_ghcr_image(
    org: str,
    image: str,
) -> dict:
    """Check a GHCR image by requesting its tag list.

    Two-step flow:
    1. Obtain a Bearer token from ``ghcr.io/token`` (anonymous scope pull).
    2. ``GET https://ghcr.io/v2/<org>/<image>/tags/list`` with auth header.

    Returns
    -------
    dict
        ``reachable``, ``tags`` (list of str), ``status_code``,
        ``org``, ``image``.
    """
    base: dict = {"org": org, "image": image}

    # ── Step 1: acquire anonymous Bearer token ───────────────────────
    token_url = (
        f"https://ghcr.io/token"
        f"?scope=repository:{org}/{image}:pull"
        f"&service=ghcr.io"
    )
    status, body, _headers = _retry_with_backoff(
        lambda: _http_get(token_url, timeout=10.0)
    )
    token: str = ""
    if status == 200:
        try:
            token_data = json.loads(body)
            token = token_data.get("token", "")
        except json.JSONDecodeError:
            logger.error("Malformed GHCR token response for %s/%s", org, image)

    if not token:
        # Cannot obtain token — the repo may be private, or auth is required.
        # Fall through to a token-less probe.
        pass

    # ── Step 2: fetch tag list (with token if we have one) ──────────
    tags_url = f"https://ghcr.io/v2/{org}/{image}/tags/list"
    req_headers: dict[str, str] = {}
    if token:
        req_headers["Authorization"] = f"Bearer {token}"

    status, body, _headers = _retry_with_backoff(
        lambda: _http_get(tags_url, headers=req_headers, timeout=10.0)
    )

    if status == 200:
        try:
            data = json.loads(body)
            return {
                **base,
                "reachable": True,
                "tags": data.get("tags", []),
                "status_code": status,
            }
        except json.JSONDecodeError:
            logger.error(
                "Malformed JSON from GHCR for %s/%s",
                org,
                image,
            )
            return {**base, "reachable": False, "tags": [], "status_code": status}
    else:
        return {**base, "reachable": False, "tags": [], "status_code": status}
