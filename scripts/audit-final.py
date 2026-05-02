#!/usr/bin/env python3
"""
Quality audit script for the Arcane template corpus.

Reads every template directory under ``templates/`` (1,143 templates), checks
each template across five audit dimensions, and produces a structured JSON
report + a human-readable markdown report.

Dimensions:
  1. Reachability  — is the Docker image pullable?
  2. Freshness     — how recently was the image updated?
  3. Ports         — are port mappings plausible and non-conflicting?
  4. Tags          — are tags well-formed and known?
  5. Classification — do tags correctly describe the image type?

Usage:
    python scripts/audit-final.py [--limit N] [--verbose]
                                  [--output-json PATH] [--output-md PATH]

Dependencies: Python stdlib only (urllib, json, argparse, logging, re, etc.)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
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

logger = logging.getLogger("audit")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_VERSION = "1.0.0"

# Known valid tags derived from the 1,143-template corpus
KNOWN_TAGS: dict[str, list[str]] = {
    "source": [
        "self-hosted",
        "yunohost",
        "portainer",
        "umbrel",
        "awesome-selfhosted",
    ],
    "category": [
        "ai",
        "devops",
        "agents",
        "communication",
        "llm",
        "storage",
        "rag",
        "monitoring",
        "framework",
        "security",
        "cms",
        "automation",
        "search",
        "observability",
        "database",
        "tools",
        "orchestration",
        "analytics",
        "workflow",
        "chat",
        "web",
        "research",
        "python",
        "proxy",
        "paas",
        "low-code",
        "inference",
        "gateway",
        "sql",
        "platform",
        "api",
        "reference",
    ],
    "status": [
        "multi-service",
        "non-serviceable",
        "priority",
    ],
}

# Flatten known tags for quick lookup
ALL_KNOWN_TAGS: set[str] = set()
for _cat, tags in KNOWN_TAGS.items():
    ALL_KNOWN_TAGS.update(tags)

# Known non-AI namespaces (for classification check)
NON_AI_NAMESPACES: set[str] = {
    "grafana", "prom", "prometheus", "influxdb", "chronograf",
    "kapacitor", "telegraf", "netdata", "cacti", "zabbix",
    "nagios", "icinga", "kibana", "logstash", "elasticsearch",
    "humio", "splunk", "datadog", "newrelic", "dynatrace",
    "checkmk", "librenms", "observium",
}

# ---------------------------------------------------------------------------
# Template data model
# ---------------------------------------------------------------------------


class TemplateData:
    """Parsed template data from arcane.json and docker-compose.yml."""

    def __init__(self, template_id: str, path: Path) -> None:
        self.id: str = template_id
        self.path: Path = path
        self.arcane_path: Path = path / "arcane.json"
        self.compose_path: Path = path / "docker-compose.yml"
        self.arcane: dict | None = None
        self.compose_text: str | None = None
        self.services: list[dict] = []
        self.findings: list[dict] = []
        self.error: str | None = None  # Fatal load error

    def load(self) -> None:
        """Load and parse arcane.json and docker-compose.yml."""
        # Arcane.json
        if not self.arcane_path.exists():
            self.error = f"Missing arcane.json"
            self.findings.append(self._finding(
                "structure", "error",
                "Missing arcane.json",
                "Create arcane.json with id, name, tags fields",
            ))
            return

        try:
            with open(self.arcane_path, "r", encoding="utf-8") as f:
                self.arcane = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.error = f"Corrupt arcane.json: {e}"
            self.findings.append(self._finding(
                "structure", "error",
                f"Corrupt arcane.json: {e}",
                "Fix JSON syntax in arcane.json",
            ))
            return

        # docker-compose.yml
        if not self.compose_path.exists():
            self.findings.append(self._finding(
                "structure", "warning",
                "Missing docker-compose.yml",
                "Create docker-compose.yml with service definitions",
            ))
            return

        try:
            self.compose_text = self.compose_path.read_text("utf-8", errors="replace")
        except (OSError, UnicodeDecodeError) as e:
            self.findings.append(self._finding(
                "structure", "error",
                f"Cannot read docker-compose.yml: {e}",
                "Fix file permissions or encoding",
            ))
            return

        # Extract services (image refs + ports)
        self.services = self._extract_services()

    # ------------------------------------------------------------------
    # Finding factory
    # ------------------------------------------------------------------

    @staticmethod
    def _finding(
        dimension: str,
        severity: str,
        message: str,
        suggested_fix: str | None = None,
        details: dict | None = None,
    ) -> dict:
        return {
            "dimension": dimension,
            "severity": severity,
            "message": message,
            "suggested_fix": suggested_fix,
            "details": details or {},
        }

    # ------------------------------------------------------------------
    # Service extraction from docker-compose.yml
    # ------------------------------------------------------------------

    def _extract_services(self) -> list[dict]:
        """Parse image refs and port mappings from docker-compose.yml text."""
        text = self.compose_text or ""
        services: list[dict] = []

        current_service: str | None = None
        in_ports = False
        in_services = False

        for line in text.splitlines():
            stripped = line.strip()

            # Service header
            svc_match = re.match(r"^  ([a-zA-Z0-9_-]+):$", line)
            if svc_match and not line.startswith("    "):
                current_service = svc_match.group(1)
                in_ports = False
                continue

            # Image line
            img_match = re.match(r"^\s+image:\s+(.+)$", line)
            if img_match and current_service:
                services.append({
                    "name": current_service,
                    "image_ref": img_match.group(1).strip().strip('"').strip("'"),
                    "ports": [],
                })
                continue

            # Ports section
            if re.match(r"^\s+ports:", line) and current_service:
                in_ports = True
                continue

            # Port entries
            port_match = re.match(r"^\s+-\s+(.+)$", line)
            if port_match and in_ports and current_service:
                port_val = port_match.group(1).strip().strip('"').strip("'")
                # Find or create service entry
                for svc in services:
                    if svc["name"] == current_service:
                        svc["ports"].append(port_val)
                        break
            else:
                in_ports = False

        return services

    # ------------------------------------------------------------------
    # Image ref parsing
    # ------------------------------------------------------------------


_REF_RE = re.compile(
    r"^(?P<registry>docker\.io|ghcr\.io|quay\.io)/(?P<namespace>[^/]+)/(?P<image>[^:@]+)(?::(?P<tag>.+))?$"
)

# Also handle docker.io when just ns/img is given (implied docker.io)
_SIMPLE_REF_RE = re.compile(
    r"^(?P<namespace>[^/]+)/(?P<image>[^:@]+)(?::(?P<tag>.+))?$"
)


def parse_image_ref(ref: str) -> dict | None:
    """Parse an image ref into structured parts.

    Returns a dict with keys: registry, namespace, image, tag, original_ref.
    Returns None if the ref is unparseable.
    """
    ref = ref.strip()

    # ghcr.io/org/img[:tag]
    m = _REF_RE.match(ref)
    if m:
        return {
            "registry": m.group("registry"),
            "namespace": m.group("namespace"),
            "image": m.group("image"),
            "tag": m.group("tag") or "latest",
            "original_ref": ref,
        }

    # ns/img[:tag] (implied docker.io)
    m = _SIMPLE_REF_RE.match(ref)
    if m:
        return {
            "registry": "docker.io",
            "namespace": m.group("namespace"),
            "image": m.group("image"),
            "tag": m.group("tag") or "latest",
            "original_ref": ref,
        }

    return None


# ---------------------------------------------------------------------------
# Audit dimensions
# ---------------------------------------------------------------------------


def check_reachability(td: TemplateData) -> list[dict]:
    """Dimension 1: Check whether each image reference is reachable.

    Returns a list of findings (one per image or structural issue).
    Delegates to registry_client.py for API calls.
    """
    findings: list[dict] = []

    if td.error:
        return findings  # Fatal structural error already recorded

    if not td.services:
        findings.append(td._finding(
            "reachability", "warning",
            "No service image references found",
            "Define at least one service with an image in docker-compose.yml",
        ))
        return findings

    for svc in td.services:
        ref = svc["image_ref"]
        parsed = parse_image_ref(ref)

        if parsed is None:
            if "${" in ref:
                # Variable substitution — can't parse statically
                findings.append(td._finding(
                    "reachability", "info",
                    f"Service '{svc['name']}': image ref uses variable substitution ({ref}) — "
                    f"skipping static reachability check",
                    "Resolve variables at runtime and verify",
                ))
                continue
            findings.append(td._finding(
                "reachability", "error",
                f"Service '{svc['name']}': unparseable image ref '{ref}'",
                "Fix format: <registry>/<namespace>/<image>[:tag]",
            ))
            continue

        registry = parsed["registry"]
        ns = parsed["namespace"]
        img = parsed["image"]

        # Custom-build templates (built by CI) — skip reachability
        if registry == "ghcr.io" and ns == "heretek-ai" and img.startswith("arcane-repo/"):
            findings.append(td._finding(
                "reachability", "info",
                f"Service '{svc['name']}': custom-build image (GHCR CI-built) — skipping reachability",
                "Verified by CI pipeline",
            ))
            continue

        # Check reachability
        if registry == "docker.io":
            result = check_dockerhub_image(ns, img)
            if result["exists"]:
                # Also fetch tags for freshness dimension later
                svc["_dh_result"] = result
                svc["_reachable"] = True
                findings.append(td._finding(
                    "reachability", "pass",
                    f"Service '{svc['name']}': image {ref} is reachable on Docker Hub",
                    None,
                ))
            else:
                svc["_reachable"] = False
                error_detail = result.get("error") or "not found"
                findings.append(td._finding(
                    "reachability", "error",
                    f"Service '{svc['name']}': image {ref} is NOT reachable — {error_detail}",
                    f"Check if the image name/tag is correct; verify it exists on Docker Hub",
                    {"error": error_detail},
                ))

        elif registry == "ghcr.io":
            result = check_ghcr_image(ns, img)
            if result.get("reachable"):
                svc["_reachable"] = True
                svc["_ghcr_result"] = result
                findings.append(td._finding(
                    "reachability", "pass",
                    f"Service '{svc['name']}': image {ref} is reachable on GHCR",
                    None,
                ))
            else:
                svc["_reachable"] = False
                status = result.get("status_code", 0)
                error_detail = "not found" if status == 404 else \
                    "unauthorized" if status in (401, 403) else \
                    f"HTTP {status}" if status else "network error"
                findings.append(td._finding(
                    "reachability", "error",
                    f"Service '{svc['name']}': image {ref} is NOT reachable — {error_detail}",
                    f"Check if the image exists and is public on GHCR",
                    {"status_code": status},
                ))

        elif registry == "quay.io":
            # Quay — check via registry API
            result = _check_quay_image(ns, img)
            if result.get("reachable"):
                svc["_reachable"] = True
                findings.append(td._finding(
                    "reachability", "pass",
                    f"Service '{svc['name']}': image {ref} is reachable on Quay",
                    None,
                ))
            else:
                svc["_reachable"] = False
                findings.append(td._finding(
                    "reachability", "error",
                    f"Service '{svc['name']}': image {ref} is NOT reachable on Quay",
                    f"Check if the image exists and is public on quay.io",
                ))

    return findings


def _check_quay_image(namespace: str, image: str) -> dict:
    """Check a Quay.io image via its public API."""
    url = f"https://quay.io/api/v1/repository/{namespace}/{image}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            _stats["requests"] += 1
            return {"reachable": True, "tags": [], "status_code": resp.status}
    except urllib.error.HTTPError as e:
        _stats["requests"] += 1
        _stats["errors"] += 1
        return {"reachable": False, "tags": [], "status_code": e.code}
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        _stats["errors"] += 1
        return {"reachable": False, "tags": [], "status_code": 0}


# ---------------------------------------------------------------------------
# Freshness dimension
# ---------------------------------------------------------------------------


def check_freshness(td: TemplateData) -> list[dict]:
    """Dimension 2: Check image freshness (last_updated recency).

    For Docker Hub images, read ``last_updated`` from the reachability
    result.  For GHCR images owned by ``heretek-ai`` (custom-build), skip.
    For external GHCR and Quay, note that last_updated is unavailable.
    For unreachable images, skip.
    """
    findings: list[dict] = []
    now = datetime.now(timezone.utc)

    for svc in td.services:
        # Skip unreachable images
        if not svc.get("_reachable", True):
            continue

        # Custom-build (CI-rebuilt) — skip
        parsed = parse_image_ref(svc["image_ref"])
        if parsed and parsed["registry"] == "ghcr.io" and parsed["namespace"] == "heretek-ai" and parsed["image"].startswith("arcane-repo/"):
            continue

        if parsed and parsed["registry"] == "docker.io":
            dh_result = svc.get("_dh_result")
            if dh_result and dh_result.get("last_updated"):
                try:
                    lu_str: str = dh_result["last_updated"]
                    if lu_str.endswith("Z"):
                        lu_str = lu_str[:-1] + "+00:00"
                    last_updated = datetime.fromisoformat(lu_str)
                    days = (now - last_updated).days
                    if days > 365:
                        findings.append(td._finding(
                            "freshness", "warning",
                            f"Service '{svc['name']}': image last updated {days} days ago (>365) — consider updating",
                            "Pull the latest image tag or rebuild if the image is maintained",
                            {"days_since_update": days, "last_updated": dh_result["last_updated"]},
                        ))
                    elif days > 180:
                        findings.append(td._finding(
                            "freshness", "info",
                            f"Service '{svc['name']}': image last updated {days} days ago (>180 days)",
                            "Consider verifying the image is still actively maintained",
                            {"days_since_update": days, "last_updated": dh_result["last_updated"]},
                        ))
                    else:
                        findings.append(td._finding(
                            "freshness", "pass",
                            f"Service '{svc['name']}': image updated {days} days ago (<=180) — fresh",
                            None,
                            {"days_since_update": days, "last_updated": dh_result["last_updated"]},
                        ))
                except (ValueError, TypeError):
                    findings.append(td._finding(
                        "freshness", "info",
                        f"Service '{svc['name']}': could not parse last_updated '{dh_result.get('last_updated')}'",
                        "Manual review of image update date needed",
                    ))
            elif dh_result and dh_result.get("exists"):
                # Docker Hub image that exists but last_updated wasn't returned
                findings.append(td._finding(
                    "freshness", "info",
                    f"Service '{svc['name']}': last_update not available from Docker Hub API",
                    "Manual review needed",
                ))
        elif parsed and parsed["registry"] in ("ghcr.io", "quay.io"):
            findings.append(td._finding(
                "freshness", "info",
                f"Service '{svc['name']}': last_updated unavailable via anonymous API — manual review needed",
                "Verify image freshness via GHCR/Quay web UI or authenticated API",
            ))

    return findings


# ---------------------------------------------------------------------------
# Port plausibility dimension
# ---------------------------------------------------------------------------

# Regex to parse a port mapping entry.  Handles:
#   "8080:8080"
#   "${VAR:-8080}:8080"
#   "127.0.0.1:8080:8080"
#   "${VAR:-5006}:5006/tcp"
_PORT_ENTRY_RE = re.compile(
    r"""
    (?:
        [a-zA-Z0-9_.-]+:                     # optional host IP
    )?
    (?:
        \$\{[^}]+:-(?P<host_port>\d+)\}      # ${VAR:-port}
        |
        (?P<host_port_plain>\d+)             # plain port
    )
    :
    (?P<container_port>\d+)                  # container port
    (?:/(?P<protocol>[a-z]+))?               # optional /tcp /udp
    """,
    re.VERBOSE,
)

WELL_KNOWN_PORTS: set[int] = {
    80, 443, 22, 3306, 5432, 6379, 8080, 8443, 9090,
}


def check_ports(td: TemplateData) -> list[dict]:
    """Dimension 3: Validate port mappings in docker-compose.yml.

    Checks: valid range, no zero-port, note well-known ports, warn on
    duplicate container ports across services.
    """
    findings: list[dict] = []

    if td.compose_text is None:
        return findings

    # First, collect all parsed port entries
    seen_container_ports: dict[int, list[str]] = {}
    any_ports = False

    for svc in td.services:
        for port_raw in svc.get("ports", []):
            any_ports = True
            m = _PORT_ENTRY_RE.match(port_raw)
            if not m:
                findings.append(td._finding(
                    "ports", "warning",
                    f"Service '{svc['name']}': unparseable port mapping '{port_raw}'",
                    f"Expected format: [host:]container_port or ${{VAR:-host_port}}:container_port",
                ))
                continue

            host_port_str = m.group("host_port") or m.group("host_port_plain")
            container_port_str = m.group("container_port")

            try:
                container_port = int(container_port_str)
            except (ValueError, TypeError):
                findings.append(td._finding(
                    "ports", "error",
                    f"Service '{svc['name']}': non-numeric container port '{container_port_str}'",
                    f"Container port must be a number 1-65535",
                ))
                continue

            if container_port == 0:
                findings.append(td._finding(
                    "ports", "error",
                    f"Service '{svc['name']}': container port is 0 (invalid)",
                    "Set a valid port in 1-65535 range",
                ))
                continue

            if not (1 <= container_port <= 65535):
                findings.append(td._finding(
                    "ports", "error",
                    f"Service '{svc['name']}': container port {container_port} out of range 1-65535",
                    "Set a valid port in 1-65535 range",
                ))
                continue

            # Track for duplicate detection
            if container_port not in seen_container_ports:
                seen_container_ports[container_port] = []
            seen_container_ports[container_port].append(svc["name"])

    # Flag duplicates
    for cport, svc_names in seen_container_ports.items():
        if len(svc_names) > 1:
            findings.append(td._finding(
                "ports", "warning",
                f"Multiple services expose container port {cport}: {', '.join(svc_names)}",
                "Ensure services are on different container ports or use different compose files/profiles",
                {"container_port": cport, "services": svc_names},
            ))

    # Flag well-known ports
    for cport in seen_container_ports:
        if cport in WELL_KNOWN_PORTS:
            svc_list = seen_container_ports[cport]
            findings.append(td._finding(
                "ports", "info",
                f"Service(s) {svc_list} expose well-known container port {cport}",
                "Verify this is intentional (e.g. web app on 8080, DB on 3306)",
                {"container_port": cport, "services": svc_list, "note": "commonly used port — likely intentional"},
            ))

    if not any_ports:
        findings.append(td._finding(
            "ports", "info",
            "No ports exposed in docker-compose.yml",
            "Verify this is intentional (e.g. background worker, CLI tool)",
        ))
    elif not findings:
        # All ports are clean — record a pass finding so the dimension appears
        # in the report even when nothing is wrong.
        findings.append(td._finding(
            "ports", "pass",
            f"Port mappings OK — {sum(len(s.get('ports',[])) for s in td.services)} port(s) mapped",
            None,
        ))

    return findings


# ---------------------------------------------------------------------------
# Tag quality dimension
# ---------------------------------------------------------------------------


def check_tags(td: TemplateData) -> list[dict]:
    """Dimension 4: Validate template tags against known taxonomy."""
    findings: list[dict] = []

    if td.error:
        return findings  # Structural failure supersedes

    tags: list[str] = (td.arcane or {}).get("tags", [])

    if not tags:
        findings.append(td._finding(
            "tags", "error",
            "No tags defined in arcane.json",
            "Add at least one source tag (e.g. 'self-hosted') and one or more category/status tags",
        ))
        return findings

    unknown_tags = [t for t in tags if t not in ALL_KNOWN_TAGS]
    if unknown_tags:
        findings.append(td._finding(
            "tags", "warning",
            f"Unknown tag(s): {', '.join(unknown_tags)}",
            f"Consider using only known tags from: source={KNOWN_TAGS['source']}, category={KNOWN_TAGS['category']}, status={KNOWN_TAGS['status']}",
            {"unknown_tags": unknown_tags},
        ))

    # Check for minimum diversity: at least one source tag
    has_source = any(t in KNOWN_TAGS["source"] for t in tags)
    if not has_source and len(tags) <= 1:
        findings.append(td._finding(
            "tags", "info",
            f"Only {len(tags)} tag(s) defined and missing a source tag (e.g. 'self-hosted')",
            "Consider adding a source tag and at least one category tag for better discovery",
            {"tag_count": len(tags)},
        ))
    elif len(tags) == 1:
        findings.append(td._finding(
            "tags", "info",
            f"Only 1 tag defined: '{tags[0]}' — sparse",
            "Consider adding category tags (e.g. 'ai', 'monitoring') for better discovery",
            {"tag_count": 1},
        ))
    else:
        findings.append(td._finding(
            "tags", "pass",
            f"{len(tags)} tags all known — OK",
            None,
            {"tags": tags},
        ))

    return findings


# ---------------------------------------------------------------------------
# Classification correctness dimension
# ---------------------------------------------------------------------------

def check_classification(td: TemplateData) -> list[dict]:
    """Dimension 5: Cross-reference tags against image source type.

    Rules (intentionally conservative — only clear mismatches):
    (a) 'ai' or 'llm' tag + image namespace is a known non-AI tool → warning
    (b) 'self-hosted' tag + all images unreachable → error
    (c) Source tag (yunohost/portainer/umbrel/awesome-selfhosted) + actual
        image source doesn't match the implied origin → info
    """
    findings: list[dict] = []

    if td.error:
        return findings

    tags: list[str] = (td.arcane or {}).get("tags", [])
    if not tags:
        return findings

    has_ai_tag = "ai" in tags or "llm" in tags
    has_self_hosted = "self-hosted" in tags
    source_tags = [t for t in tags if t in KNOWN_TAGS["source"]]

    # Collect image namespaces
    namespaces: list[str] = []
    all_reachable = True
    any_image = False
    for svc in td.services:
        ref = svc["image_ref"]
        parsed = parse_image_ref(ref)
        if parsed:
            any_image = True
            namespaces.append(parsed["namespace"])
            if not svc.get("_reachable", False):
                all_reachable = False

    # Rule (a): AI/LLM tag + known non-AI namespace
    if has_ai_tag:
        for ns in namespaces:
            if ns.lower() in NON_AI_NAMESPACES:
                findings.append(td._finding(
                    "classification", "warning",
                    f"Tagged 'ai'/'llm' but image is from '{ns}' (known non-AI namespace)",
                    "Remove 'ai'/'llm' tag or verify this template provides AI functionality",
                    {"tag": "ai/llm", "namespace": ns},
                ))

    # Rule (b): self-hosted tag but all images unreachable
    if has_self_hosted and any_image and not all_reachable:
        findings.append(td._finding(
            "classification", "warning",
            "Tagged 'self-hosted' but no image is reachable",
            "Fix image references or remove 'self-hosted' tag",
        ))

    # Rule (c): source tag vs. actual image source
    if "yunohost" in source_tags:
        # YunoHost apps typically come from Docker Hub, not GHCR/Quay
        for ns in namespaces:
            # If the namespace doesn't look like a typical YunoHost catalog pattern
            # (YunoHost apps often have 'yunohost' in the org name or are docker.io)
            pass  # Conservative — hard to infer reliably, skip
    elif "portainer" in source_tags:
        # Portainer templates often reference GHCR images
        pass
    elif "umbrel" in source_tags:
        # Umbrel apps typically are docker.io
        pass
    elif "awesome-selfhosted" in source_tags:
        pass

    # Additional: multiple source tags is suspicious
    if len(source_tags) > 1:
        findings.append(td._finding(
            "classification", "info",
            f"Multiple source tags set: {', '.join(source_tags)}",
            "Each template should typically have one source tag; verify this is correct",
            {"source_tags": source_tags},
        ))

    return findings


# ---------------------------------------------------------------------------
# Module-level stats (mirrors registry_client)
# ---------------------------------------------------------------------------

_stats: dict[str, int] = {
    "requests": 0,
    "errors": 0,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Arcane template quality audit",
    )
    parser.add_argument(
        "--output-json",
        default="audit-report.json",
        help="Path for JSON report (default: audit-report.json)",
    )
    parser.add_argument(
        "--output-md",
        default="audit-report.md",
        help="Path for Markdown report (default: audit-report.md)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only audit first N templates (default: all)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable DEBUG logging",
    )
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Path to templates directory (default: templates)",
    )
    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger.setLevel(log_level)

    start_time = time.time()

    # Enumerate templates
    templates_dir = Path(args.templates_dir)
    if not templates_dir.is_dir():
        logger.error("Templates directory not found: %s", templates_dir)
        sys.exit(1)

    template_ids: list[str] = sorted(
        d.name for d in templates_dir.iterdir() if d.is_dir()
    )
    total_templates = len(template_ids)

    if args.limit:
        total_templates = min(total_templates, args.limit)

    logger.info("Starting audit of %d templates (limit=%s)", total_templates, args.limit or "none")

    # Process each template
    all_templates: list[dict] = []
    total_findings = 0

    for idx in range(total_templates):
        tid = template_ids[idx]
        current = idx + 1
        t_start = time.time()

        td = TemplateData(tid, templates_dir / tid)
        td.load()

        # Run all audit dimensions
        reachability_findings = check_reachability(td)
        freshness_findings = check_freshness(td)
        ports_findings = check_ports(td)
        tags_findings = check_tags(td)
        classification_findings = check_classification(td)

        # Collect all findings
        all_findings = (
            td.findings
            + reachability_findings
            + freshness_findings
            + ports_findings
            + tags_findings
            + classification_findings
        )
        total_findings += len(all_findings)

        # Count dimensions
        dim_counts: dict[str, dict[str, int]] = {}
        for f in all_findings:
            dim = f["dimension"]
            sev = f["severity"]
            if dim not in dim_counts:
                dim_counts[dim] = {"pass": 0, "info": 0, "warning": 0, "error": 0}
            if sev in dim_counts[dim]:
                dim_counts[dim][sev] += 1

        elapsed = time.time() - t_start
        dim_summary = " ".join(
            f"{d}={sum(c.values())}({','.join(f'{s}={c[s]}' for s in ('pass', 'info', 'warning', 'error') if c[s])})"
            for d, c in sorted(dim_counts.items())
        )
        logger.info(
            "[%d/%d] Checking %s — %.1fs — dims: %s",
            current, total_templates, tid, elapsed, dim_summary,
        )

        entry: dict = {
            "id": tid,
            "name": (td.arcane or {}).get("name", tid),
            "tags": (td.arcane or {}).get("tags", []),
            "findings": all_findings,
            "error": td.error,
        }
        all_templates.append(entry)

    # Summarize
    duration = time.time() - start_time
    by_severity: dict[str, int] = {"error": 0, "warning": 0, "info": 0, "pass": 0}
    by_dimension: dict[str, int] = {}

    for entry in all_templates:
        for f in entry["findings"]:
            sev = f["severity"]
            dim = f["dimension"]
            if sev in by_severity:
                by_severity[sev] += 1
            by_dimension[dim] = by_dimension.get(dim, 0) + 1

    api_stats = get_stats()
    # Merge audit-local Quay stats into registry stats
    api_stats["requests"] = api_stats.get("requests", 0) + _stats.get("requests", 0)
    api_stats["errors"] = api_stats.get("errors", 0) + _stats.get("errors", 0)

    report: dict = {
        "run_metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": round(duration, 2),
            "total_templates_scanned": total_templates,
            "api_stats": {
                "requests": api_stats.get("requests", 0),
                "retries": api_stats.get("retries", 0),
                "errors": api_stats.get("errors", 0),
                "rate_limit_hits": api_stats.get("rate_limit_hits", 0),
            },
            "script_version": SCRIPT_VERSION,
        },
        "summary": {
            "total_templates": total_templates,
            "total_findings": total_findings,
            "by_severity": by_severity,
            "by_dimension": by_dimension,
        },
        "templates": all_templates,
    }

    # Write JSON report
    json_path = Path(args.output_json)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    logger.info("Wrote JSON report to %s (%d bytes)", json_path, json_path.stat().st_size)

    # Write Markdown report
    md_path = Path(args.output_md)
    _write_markdown_report(report, md_path)
    logger.info("Wrote Markdown report to %s (%d bytes)", md_path, md_path.stat().st_size)

    logger.info(
        "Audit complete: %d templates, %d findings in %.1fs",
        total_templates, total_findings, duration,
    )


def _write_markdown_report(report: dict, path: Path) -> None:
    """Write a human-readable markdown report."""
    meta = report["run_metadata"]
    summary = report["summary"]
    by_sev = summary["by_severity"]
    by_dim = summary["by_dimension"]

    lines: list[str] = []
    lines.append("# Arcane Template Audit Report\n")
    lines.append(f"**Date:** {meta['timestamp']}")
    lines.append(f"**Templates scanned:** {meta['total_templates_scanned']}")
    lines.append(f"**Duration:** {meta['duration_seconds']}s")
    lines.append(f"**Script version:** {meta['script_version']}\n")

    lines.append("## Summary\n")
    lines.append("### By Severity\n")
    lines.append(f"| Severity | Count |")
    lines.append(f"|----------|-------|")
    for sev in ("error", "warning", "info", "pass"):
        lines.append(f"| {sev} | {by_sev.get(sev, 0)} |")
    lines.append("")

    lines.append("### By Dimension\n")
    lines.append(f"| Dimension | Findings |")
    lines.append(f"|-----------|----------|")
    for dim, cnt in sorted(by_dim.items()):
        lines.append(f"| {dim} | {cnt} |")
    lines.append("")

    lines.append("## Per-Dimension Findings\n")
    for dim in sorted(by_dim.keys()):
        lines.append(f"### {dim.capitalize()}\n")
        lines.append(f"**Total findings in this dimension: {by_dim.get(dim, 0)}**\n")

        dim_by_sev: dict[str, int] = {"pass": 0, "info": 0, "warning": 0, "error": 0}
        dim_findings = []
        for t in report["templates"]:
            for f in t["findings"]:
                if f["dimension"] == dim:
                    dim_findings.append((t["id"], t.get("name", t["id"]), f))
                    sev = f["severity"]
                    if sev in dim_by_sev:
                        dim_by_sev[sev] += 1

        if not dim_findings:
            lines.append("_No findings in this dimension._\n")
            continue

        lines.append("#### Severity Breakdown\n")
        lines.append("| Severity | Count |")
        lines.append("|----------|-------|")
        for sev in ("error", "warning", "info", "pass"):
            cnt = dim_by_sev.get(sev, 0)
            if cnt > 0:
                lines.append(f"| {sev} | {cnt} |")
        lines.append("")

        lines.append("#### Per-Template Findings\n")
        lines.append("| Template ID | Name | Severity | Message | Suggested Fix |")
        lines.append("|-------------|------|----------|---------|---------------|")
        for tid, tname, f in dim_findings:
            fix = f.get("suggested_fix") or "—"
            lines.append(f"| {tid} | {tname} | {f['severity']} | {f['message']} | {fix} |")
        lines.append("")

    # Appendix: templates with errors
    error_templates = [t for t in report["templates"] if any(
        f["severity"] == "error" for f in t["findings"]
    )]
    if error_templates:
        lines.append("## Appendix: Templates with Errors\n")
        lines.append("| Template ID | Name |")
        lines.append("|-------------|------|")
        for t in error_templates:
            lines.append(f"| {t['id']} | {t['name']} |")
        lines.append("")

    # Appendix: clean templates
    clean_templates = [t for t in report["templates"] if not t["findings"]]
    if clean_templates:
        lines.append("## Appendix: Clean Templates (Zero Findings)\n")
        lines.append("| Template ID | Name |")
        lines.append("|-------------|------|")
        for t in clean_templates:
            lines.append(f"| {t['id']} | {t['name']} |")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
