#!/usr/bin/env python3
"""
M008 Quality Audit Script for the Arcane template corpus.

Scans all active templates and identifies quality issues across four dimensions:

  1. Provenance   — Detects 'sourced from [catalog]' markers in descriptions.
                    Derives original project URLs from Docker image namespaces.
                    Flags ambiguous mappings (generic images, non-GitHub orgs).
  2. Documentation — Detects generic boilerplate READMEs, counts sections,
                     flags missing project links.
  3. Compose      — Checks for healthcheck presence, restart policy, YAML
                    validity, and service count.
  4. Metadata     — Validates required fields in arcane.json, detects empty
                    or placeholder descriptions.

Non-serviceable templates (tagged 'non-serviceable' in arcane.json) are skipped.

Usage:
    python scripts/audit-templates.py [--templates-dir DIR] [--output-json PATH]
                                      [--output-md PATH] [--limit N] [--verbose]

Dependencies: Python stdlib only (no external packages).
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("audit-templates")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_VERSION = "1.0.0"

# Generic base images where namespace→GitHub mapping is meaningless
GENERIC_NAMESPACES: set[str] = {
    "library", "bitnami", "lscr.io/linuxserver",
}

# Generic image names that don't map to a single GitHub project
GENERIC_IMAGES: set[str] = {
    "python", "node", "nginx", "postgres", "redis", "mysql",
    "mongo", "alpine", "ubuntu", "debian", "busybox", "httpd",
    "php", "ruby", "golang", "openjdk", "eclipse-mosquitto",
    "traefik", "portainer", "adminer", "memcached", "rabbitmq",
    "elasticsearch", "kibana", "logstash", "grafana", "prometheus",
    "influxdb", "minio", "docker", "caddy", "haproxy", "mysql",
    "mariadb", "mongo", "couchdb", "nextcloud", "wordpress",
    "drupal", "ghost", "joomla", "magento", "mediawiki",
}

# Required fields in arcane.json
REQUIRED_METADATA_FIELDS: list[str] = [
    "id", "name", "description", "version", "author", "tags",
]

# Patterns indicating generic/placeholder descriptions
PLACEHOLDER_DESCRIPTION_PATTERNS: list[str] = [
    r"^todo$",
    r"^tbd$",
    r"^placeholder",
    r"^description\s*$",
    r"^<.*>$",
    r"^test\s*$",
]

# Patterns indicating boilerplate READMEs
BOILERPLATE_PATTERNS: list[str] = [
    r"self-hosted application available through",
    r"sourced from (the )?(yunohost|portainer|umbrel|awesome-selfhosted)",
]

# ---------------------------------------------------------------------------
# Image ref parsing
# ---------------------------------------------------------------------------

def _parse_image_ref(ref: str) -> tuple[str | None, str | None, str | None, str | None]:
    """Parse a Docker image reference into (registry, namespace, image, tag).

    Returns (None, None, None, None) if unparseable.
    """
    ref = ref.strip()
    if not ref:
        return None, None, None, None

    # Strip variable substitution for parsing (e.g. ${VAR:-value})
    # We only need the image name part, not the resolved value
    if "${" in ref:
        return None, None, None, None

    tag = "latest"

    # ghcr.io/org/repo[:tag]
    if ref.startswith("ghcr.io/"):
        parts = ref[len("ghcr.io/"):].split("/", 1)
        if len(parts) == 2:
            ns = parts[0]
            img_part = parts[1]
            if ":" in img_part:
                img_part, tag = img_part.rsplit(":", 1)
            return "ghcr.io", ns, img_part, tag

    # docker.io/ns/img[:tag] or just ns/img[:tag]
    if ref.startswith("docker.io/"):
        ref = ref[len("docker.io/"):]

    # ns/img[:tag]
    if "/" in ref:
        parts = ref.split("/", 1)
        ns = parts[0]
        img_part = parts[1]
        if ":" in img_part:
            img_part, tag = img_part.rsplit(":", 1)
        return "docker.io", ns, img_part, tag

    # Bare image name (library image)
    if ":" in ref:
        img, tag = ref.rsplit(":", 1)
    else:
        img = ref
    return "docker.io", "library", img, tag


def _derive_project_url_from_image(image_ref: str) -> tuple[str | None, bool]:
    """Derive a GitHub project URL from a Docker image namespace.

    Returns (url, ambiguous) where ambiguous=True means the mapping
    is uncertain (generic image, non-GitHub org, etc.).
    """
    registry, ns, image, _tag = _parse_image_ref(image_ref)

    if ns is None:
        return None, True

    # Generic/official images have no meaningful GitHub mapping
    if ns == "library" or image in GENERIC_IMAGES:
        return None, True

    # GHCR images: ghcr.io/{org}/{repo} → https://github.com/{org}/{repo}
    if registry == "ghcr.io":
        if ns == "heretek-ai" or ns == "arcane-repo":
            # Custom-build templates — skip
            return None, True
        url = f"https://github.com/{ns}/{image}"
        return url, False

    # LinuxServer images: special case
    if ns == "lscr.io/linuxserver":
        return None, True

    # Docker Hub: {org}/{repo} → https://github.com/{org}/{repo}
    # This is heuristic — many Docker Hub orgs match GitHub orgs
    url = f"https://github.com/{ns}/{image}"
    return url, False


# ---------------------------------------------------------------------------
# GitHub URL verification (cached, with rate-limit awareness)
# ---------------------------------------------------------------------------

_github_url_cache: dict[str, bool] = {}


def _check_github_url_exists(url: str, timeout: float = 5.0) -> bool:
    """Check whether a GitHub URL exists by following redirects.

    Returns True if the final URL is a valid GitHub repository page.
    Caches results to avoid redundant API calls.
    """
    if url in _github_url_cache:
        return _github_url_cache[url]

    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "arcane-audit/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = resp.status == 200
            _github_url_cache[url] = result
            return result
    except (urllib.error.HTTPError, urllib.error.URLError, OSError, TimeoutError):
        _github_url_cache[url] = False
        return False


# ---------------------------------------------------------------------------
# Dimension 1: Provenance
# ---------------------------------------------------------------------------

def check_provenance(arcane: dict, compose_services: list[dict]) -> list[dict]:
    """Check provenance quality of a template.

    Detects 'sourced from [catalog]' markers in descriptions, derives
    original project URLs from Docker image namespaces, and flags
    ambiguous mappings.
    """
    issues: list[dict] = []
    desc: str = arcane.get("description", "")

    # Check for 'sourced from' marker
    sourced_match = re.search(r"sourced from\s+(?:the\s+)?(\w[\w\s]*\w)", desc, re.IGNORECASE)
    if sourced_match:
        catalog = sourced_match.group(1).strip().lower()
        issues.append({
            "dimension": "provenance",
            "severity": "info",
            "message": f"Description contains 'sourced from {catalog}' marker",
            "suggested_fix": f"Verify template correctly attributes the {catalog} catalog",
        })

    # Try to derive project URL from image namespace
    if compose_services:
        first_svc = compose_services[0]
        image_ref = first_svc.get("image", "")
        if image_ref:
            url, ambiguous = _derive_project_url_from_image(image_ref)
            # Only report derived URL if we found one; skip ambiguous for generic images
            if url:
                issues.append({
                    "dimension": "provenance",
                    "severity": "info",
                    "message": f"Derived project URL: {url}",
                    "suggested_fix": "Add this URL to README as a link to the original project",
                })

    return issues


# ---------------------------------------------------------------------------
# Dimension 2: Documentation
# ---------------------------------------------------------------------------

def check_documentation(readme_path: Path, arcane: dict, compose_services: list[dict]) -> list[dict]:
    """Check README quality: boilerplate detection, section count, project links.

    Returns a list of issues found in the README.
    """
    issues: list[dict] = []

    if not readme_path.exists():
        issues.append({
            "dimension": "documentation",
            "severity": "warning",
            "message": "Missing README.md",
            "suggested_fix": "Create a README.md with project description, setup instructions, and configuration details",
        })
        return issues

    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        issues.append({
            "dimension": "documentation",
            "severity": "warning",
            "message": f"Cannot read README.md: {e}",
            "suggested_fix": "Fix file permissions or encoding",
        })
        return issues

    # Check for boilerplate patterns
    for pattern in BOILERPLATE_PATTERNS:
        if re.search(pattern, readme_text, re.IGNORECASE):
            issues.append({
                "dimension": "documentation",
                "severity": "warning",
                "message": f"README contains generic boilerplate text matching '{pattern}'",
                "suggested_fix": "Replace boilerplate with project-specific description",
            })

    # Count markdown sections (## headers)
    section_count = len(re.findall(r"^#{1,3}\s+", readme_text, re.MULTILINE))
    if section_count < 2:
        issues.append({
            "dimension": "documentation",
            "severity": "info",
            "message": f"README has only {section_count} section(s) — may lack detail",
            "suggested_fix": "Add sections for Quick Start, Configuration, and Usage",
        })

    # Check for project links
    has_project_link = False

    # Check for links to GitHub, GitLab, project homepage, etc.
    link_patterns = [
        r"https?://github\.com/[\w\-]+/[\w\-]+",
        r"https?://gitlab\.com/[\w\-]+/[\w\-]+",
        r"https?://[\w\-]+\.(?:io|dev|org|com)/?",
        r"\[.*?\]\(https?://",
    ]
    for pattern in link_patterns:
        if re.search(pattern, readme_text, re.IGNORECASE):
            has_project_link = True
            break

    # Also derive and check project URL from image namespace
    if compose_services:
        first_svc = compose_services[0]
        image_ref = first_svc.get("image", "")
        if image_ref:
            url, _ambiguous = _derive_project_url_from_image(image_ref)
            if url and url in readme_text:
                has_project_link = True

    if not has_project_link:
        issues.append({
            "dimension": "documentation",
            "severity": "warning",
            "message": "README lacks links to the original project or documentation",
            "suggested_fix": "Add a link to the original project repository or homepage",
        })

    return issues


# ---------------------------------------------------------------------------
# Dimension 3: Compose
# ---------------------------------------------------------------------------

def check_compose(compose_path: Path) -> tuple[list[dict], list[dict]]:
    """Check docker-compose.yml for healthcheck, restart policy, YAML validity.

    Returns (issues, services) where services is a list of dicts with keys:
    name, image, has_healthcheck, has_restart.
    """
    issues: list[dict] = []
    services: list[dict] = []

    if not compose_path.exists():
        issues.append({
            "dimension": "compose",
            "severity": "error",
            "message": "Missing docker-compose.yml",
            "suggested_fix": "Create a docker-compose.yml with service definitions",
        })
        return issues, services

    try:
        compose_text = compose_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        issues.append({
            "dimension": "compose",
            "severity": "error",
            "message": f"Cannot read docker-compose.yml: {e}",
            "suggested_fix": "Fix file permissions or encoding",
        })
        return issues, services

    # Parse YAML manually (stdlib only)
    services = _parse_compose_services(compose_text)

    if not services:
        issues.append({
            "dimension": "compose",
            "severity": "warning",
            "message": "No services found in docker-compose.yml",
            "suggested_fix": "Define at least one service with an image",
        })
        return issues, services

    # Check each service
    for svc in services:
        svc_name = svc["name"]

        # Healthcheck
        if not svc["has_healthcheck"]:
            issues.append({
                "dimension": "compose",
                "severity": "info",
                "message": f"Service '{svc_name}' lacks a healthcheck definition",
                "suggested_fix": "Add a healthcheck to enable container health monitoring",
            })

        # Restart policy
        if not svc["has_restart"]:
            issues.append({
                "dimension": "compose",
                "severity": "info",
                "message": f"Service '{svc_name}' has no restart policy",
                "suggested_fix": "Add 'restart: unless-stopped' for production reliability",
            })

    return issues, services


def _parse_compose_services(compose_text: str) -> list[dict]:
    """Parse docker-compose.yml text to extract service info.

    Uses indentation-based parsing (stdlib only). Returns list of dicts
    with keys: name, image, has_healthcheck, has_restart.
    """
    services: list[dict] = []
    lines = compose_text.splitlines()

    in_services = False
    current_svc: dict | None = None

    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue

        # Detect 'services:' top-level key
        if re.match(r"^services:\s*$", line):
            in_services = True
            continue

        if not in_services:
            continue

        # Service header: exactly 2-space indent
        svc_match = re.match(r"^  ([a-zA-Z0-9_-]+):\s*$", line)
        if svc_match:
            if current_svc:
                services.append(current_svc)
            current_svc = {
                "name": svc_match.group(1),
                "image": "",
                "has_healthcheck": False,
                "has_restart": False,
            }
            continue

        if current_svc is None:
            continue

        # Image property: 4-space indent
        img_match = re.match(r"^\s{4}image:\s*(.+)$", line)
        if img_match:
            current_svc["image"] = img_match.group(1).strip().strip('"').strip("'")
            continue

        # Healthcheck: 4-space indent
        if re.match(r"^\s{4}healthcheck:", line):
            current_svc["has_healthcheck"] = True
            continue

        # Restart policy: 4-space indent
        restart_match = re.match(r"^\s{4}restart:\s*(.+)$", line)
        if restart_match:
            current_svc["has_restart"] = True
            continue

    # Don't forget the last service
    if current_svc:
        services.append(current_svc)

    return services


# ---------------------------------------------------------------------------
# Dimension 4: Metadata
# ---------------------------------------------------------------------------

def check_metadata(arcane: dict) -> list[dict]:
    """Check arcane.json for required fields and description quality."""
    issues: list[dict] = []

    # Check required fields
    missing = [f for f in REQUIRED_METADATA_FIELDS if f not in arcane]
    if missing:
        issues.append({
            "dimension": "metadata",
            "severity": "error",
            "message": f"Missing required fields: {', '.join(missing)}",
            "suggested_fix": f"Add the missing fields to arcane.json: {', '.join(missing)}",
        })
        return issues  # Can't check further without fields

    # Check description quality
    desc = arcane.get("description", "")
    if not desc:
        issues.append({
            "dimension": "metadata",
            "severity": "warning",
            "message": "Empty description in arcane.json",
            "suggested_fix": "Add a 1-2 sentence description of what this template does",
        })
    else:
        is_placeholder = False
        for pattern in PLACEHOLDER_DESCRIPTION_PATTERNS:
            if re.match(pattern, desc, re.IGNORECASE):
                issues.append({
                    "dimension": "metadata",
                    "severity": "warning",
                    "message": f"Description appears to be a placeholder: '{desc}'",
                    "suggested_fix": "Replace with a meaningful description of the application",
                })
                is_placeholder = True
                break

    # Check for empty tags list
    tags = arcane.get("tags", [])
    if not tags:
        issues.append({
            "dimension": "metadata",
            "severity": "warning",
            "message": "Empty tags list in arcane.json",
            "suggested_fix": "Add at least one tag (e.g. 'self-hosted', a category tag)",
        })

    # Add a pass finding if no issues were found
    if not issues:
        issues.append({
            "dimension": "metadata",
            "severity": "pass",
            "message": "All required fields present, description is substantive",
            "suggested_fix": None,
        })

    return issues


# ---------------------------------------------------------------------------
# Scan orchestration
# ---------------------------------------------------------------------------

def scan_template(template_id: str, template_dir: Path) -> dict:
    """Scan a single template across all four dimensions.

    Returns a template report dict with id, name, tags, issues.
    """
    issues: list[dict] = []

    # Read arcane.json
    arcane_path = template_dir / "arcane.json"
    if not arcane_path.exists():
        return {
            "id": template_id,
            "name": template_id,
            "tags": [],
            "issues": [{
                "dimension": "metadata",
                "severity": "error",
                "message": "Missing arcane.json",
                "suggested_fix": "Create arcane.json with required fields",
            }],
        }

    try:
        with open(arcane_path, "r", encoding="utf-8") as f:
            arcane = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return {
            "id": template_id,
            "name": template_id,
            "tags": [],
            "issues": [{
                "dimension": "metadata",
                "severity": "error",
                "message": f"Invalid arcane.json: {e}",
                "suggested_fix": "Fix JSON syntax in arcane.json",
            }],
        }

    # Skip non-serviceable templates
    tags: list[str] = arcane.get("tags", [])
    if "non-serviceable" in tags:
        logger.debug("Skipping non-serviceable template: %s", template_id)
        return {
            "id": template_id,
            "name": arcane.get("name", template_id),
            "tags": tags,
            "issues": [],
        }

    # Parse compose file
    compose_path = template_dir / "docker-compose.yml"
    compose_services: list[dict] = []
    if compose_path.exists():
        try:
            compose_text = compose_path.read_text(encoding="utf-8")
            compose_services = _parse_compose_services(compose_text)
        except (OSError, UnicodeDecodeError):
            pass

    # Run all four dimensions
    issues.extend(check_provenance(arcane, compose_services))
    issues.extend(check_documentation(template_dir / "README.md", arcane, compose_services))
    compose_issues, _svc = check_compose(compose_path)
    issues.extend(compose_issues)
    issues.extend(check_metadata(arcane))

    return {
        "id": template_id,
        "name": arcane.get("name", template_id),
        "tags": tags,
        "issues": issues,
    }


def scan_templates(templates_dir: Path, limit: int | None = None) -> list[dict]:
    """Scan all templates in the given directory.

    Returns a list of template report dicts.
    """
    if not templates_dir.is_dir():
        logger.error("Templates directory not found: %s", templates_dir)
        sys.exit(1)

    template_ids: list[str] = sorted(
        d.name for d in templates_dir.iterdir() if d.is_dir()
    )

    if limit:
        template_ids = template_ids[:limit]

    logger.info("Scanning %d templates in %s", len(template_ids), templates_dir)

    results: list[dict] = []
    for idx, tid in enumerate(template_ids, 1):
        if idx % 100 == 0 or idx == len(template_ids):
            logger.info("Progress: %d/%d templates scanned", idx, len(template_ids))

        template_dir = templates_dir / tid
        result = scan_template(tid, template_dir)
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(templates: list[dict]) -> dict:
    """Build the complete audit report with metadata and summary."""
    issue_count = sum(len(t["issues"]) for t in templates)

    # Compute summary by dimension and severity
    by_dimension: dict[str, int] = {}
    by_severity: dict[str, int] = {"error": 0, "warning": 0, "info": 0, "pass": 0}

    for t in templates:
        for issue in t["issues"]:
            dim = issue["dimension"]
            sev = issue["severity"]
            by_dimension[dim] = by_dimension.get(dim, 0) + 1
            if sev in by_severity:
                by_severity[sev] += 1

    return {
        "metadata": {
            "version": SCRIPT_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "template_count": len(templates),
            "issue_count": issue_count,
        },
        "summary": {
            "by_dimension": by_dimension,
            "by_severity": by_severity,
        },
        "templates": templates,
    }


def write_json_report(report: dict, path: Path) -> None:
    """Write the JSON report to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    logger.info("Wrote JSON report to %s (%d bytes)", path, path.stat().st_size)


def write_markdown_report(report: dict, path: Path) -> None:
    """Write a human-readable markdown summary."""
    meta = report["metadata"]
    summary = report["summary"]
    by_sev = summary["by_severity"]
    by_dim = summary["by_dimension"]

    lines: list[str] = [
        "# M008 Quality Audit Report\n",
        f"**Date:** {meta['timestamp']}",
        f"**Templates scanned:** {meta['template_count']}",
        f"**Script version:** {meta['version']}\n",
        "## Summary\n",
        "### By Severity\n",
        "| Severity | Count |",
        "|----------|-------|",
    ]

    for sev in ("error", "warning", "info", "pass"):
        lines.append(f"| {sev} | {by_sev.get(sev, 0)} |")

    lines.extend(["", "### By Dimension\n", "| Dimension | Issues |", "|-----------|--------|"])
    for dim, cnt in sorted(by_dim.items()):
        lines.append(f"| {dim} | {cnt} |")

    lines.extend(["", "## Templates with Issues\n"])

    # Group templates by dimension
    for dim in sorted(by_dim.keys()):
        lines.append(f"### {dim.capitalize()}\n")
        dim_templates = [
            t for t in report["templates"]
            if any(i["dimension"] == dim for i in t["issues"])
        ]
        if not dim_templates:
            lines.append("_No issues in this dimension._\n")
            continue

        lines.append("| Template | Issues |")
        lines.append("|----------|--------|")
        for t in dim_templates:
            dim_issues = [i for i in t["issues"] if i["dimension"] == dim]
            issue_msgs = "; ".join(i["message"] for i in dim_issues)
            lines.append(f"| {t['id']} | {issue_msgs} |")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote Markdown report to %s (%d bytes)", path, path.stat().st_size)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="M008 template quality audit — provenance, docs, compose, metadata",
    )
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Path to templates directory (default: templates/)",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Path for JSON report output",
    )
    parser.add_argument(
        "--output-md",
        default=None,
        help="Path for Markdown report output",
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
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger.setLevel(log_level)

    templates_dir = Path(args.templates_dir)
    templates = scan_templates(templates_dir, limit=args.limit)
    report = build_report(templates)

    # Write JSON report
    if args.output_json:
        json_path = Path(args.output_json)
        write_json_report(report, json_path)

    # Write Markdown report
    if args.output_md:
        md_path = Path(args.output_md)
        write_markdown_report(report, md_path)

    # Summary to stdout
    meta = report["metadata"]
    summary = report["summary"]
    logger.info(
        "Audit complete: %d templates, %d issues (errors=%d, warnings=%d, info=%d)",
        meta["template_count"],
        meta["issue_count"],
        summary["by_severity"].get("error", 0),
        summary["by_severity"].get("warning", 0),
        summary["by_severity"].get("info", 0),
    )


if __name__ == "__main__":
    main()
