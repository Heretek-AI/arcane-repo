#!/usr/bin/env python3
"""
M008 Remediation Wave Script — batch template remediation infrastructure.

Reads the S01 audit report, filters templates with documentation warnings,
splits them into batch files of 10 templates each, and generates per-template
remediation instructions for subagent processing.

Each batch file becomes the input for a subagent that will fix the template's
arcane.json, docker-compose.yml, and README.md.

Usage:
    python scripts/remediate-wave.py --audit-report PATH --batch-dir DIR
                                      [--wave N] [--batch-size N] [--dry-run]

Dependencies: Python stdlib only (no external packages).
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

logger = logging.getLogger("remediate-wave")
logger.setLevel(logging.INFO)

SCRIPT_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Image ref parsing (reused from audit-templates.py)
# ---------------------------------------------------------------------------

def _parse_image_ref(ref: str) -> tuple[str | None, str | None, str | None, str | None]:
    """Parse a Docker image reference into (registry, namespace, image, tag)."""
    ref = ref.strip()
    if not ref:
        return None, None, None, None
    if "${" in ref:
        return None, None, None, None

    tag = "latest"

    if ref.startswith("ghcr.io/"):
        parts = ref[len("ghcr.io/"):].split("/", 1)
        if len(parts) == 2:
            ns = parts[0]
            img_part = parts[1]
            if ":" in img_part:
                img_part, tag = img_part.rsplit(":", 1)
            return "ghcr.io", ns, img_part, tag

    if ref.startswith("docker.io/"):
        ref = ref[len("docker.io/"):]

    if "/" in ref:
        parts = ref.split("/", 1)
        ns = parts[0]
        img_part = parts[1]
        if ":" in img_part:
            img_part, tag = img_part.rsplit(":", 1)
        return "docker.io", ns, img_part, tag

    if ":" in ref:
        img, tag = ref.rsplit(":", 1)
    else:
        img = ref
    return "docker.io", "library", img, tag


GENERIC_NAMESPACES: set[str] = {"library", "bitnami", "lscr.io/linuxserver"}
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


def _derive_project_url(image_ref: str) -> tuple[str | None, bool]:
    """Derive a GitHub project URL from a Docker image namespace."""
    registry, ns, image, _tag = _parse_image_ref(image_ref)
    if ns is None:
        return None, True
    if ns == "library" or image in GENERIC_IMAGES:
        return None, True
    if registry == "ghcr.io":
        if ns in ("heretek-ai", "arcane-repo"):
            return None, True
        return f"https://github.com/{ns}/{image}", False
    if ns == "lscr.io/linuxserver":
        return None, True
    return f"https://github.com/{ns}/{image}", False


# ---------------------------------------------------------------------------
# Compose parsing (reused from audit-templates.py)
# ---------------------------------------------------------------------------

def _parse_compose_services(compose_text: str) -> list[dict]:
    """Parse docker-compose.yml to extract service info."""
    services: list[dict] = []
    lines = compose_text.splitlines()
    in_services = False
    current_svc: dict | None = None

    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if re.match(r"^services:\s*$", line):
            in_services = True
            continue
        if not in_services:
            continue

        svc_match = re.match(r"^  ([a-zA-Z0-9_-]+):\s*$", line)
        if svc_match:
            if current_svc:
                services.append(current_svc)
            current_svc = {
                "name": svc_match.group(1),
                "image": "",
                "has_healthcheck": False,
                "has_restart": False,
                "ports": [],
            }
            continue

        if current_svc is None:
            continue

        img_match = re.match(r"^\s{4}image:\s*(.+)$", line)
        if img_match:
            current_svc["image"] = img_match.group(1).strip().strip('"').strip("'")
            continue

        if re.match(r"^\s{4}healthcheck:", line):
            current_svc["has_healthcheck"] = True
            continue

        restart_match = re.match(r"^\s{4}restart:\s*(.+)$", line)
        if restart_match:
            current_svc["has_restart"] = True
            continue

        # Detect port mappings to identify web apps
        port_match = re.match(r"^\s+-\s+[\"']?\$\{.*?:(\d+)\}:(\d+)[\"']?\s*$", line)
        if port_match:
            current_svc["ports"].append({
                "host_default": int(port_match.group(1)),
                "container": int(port_match.group(2)),
            })
            continue

        port_match2 = re.match(r"^\s+-\s+[\"']?(\d+):(\d+)[\"']?\s*$", line)
        if port_match2:
            current_svc["ports"].append({
                "host_default": int(port_match2.group(1)),
                "container": int(port_match2.group(2)),
            })
            continue

    if current_svc:
        services.append(current_svc)

    return services


# ---------------------------------------------------------------------------
# Service type detection for healthcheck patterns
# ---------------------------------------------------------------------------

# Known service image patterns → healthcheck type
SERVICE_HEALTHCHECK_MAP: list[tuple[str, str, str]] = [
    # (image substring, healthcheck type, healthcheck command)
    ("redis", "redis", '["CMD", "redis-cli", "ping"]'),
    ("postgres", "postgres", '["CMD", "pg_isready", "-U", "${POSTGRES_USER:-app}"]'),
    ("mongo", "mongo", '["CMD", "mongosh", "--eval", "db.adminCommand(\'ping\')", "--quiet"]'),
    ("mysql", "mysql", '["CMD", "mysqladmin", "ping", "-h", "localhost"]'),
    ("mariadb", "mysql", '["CMD", "mysqladmin", "ping", "-h", "localhost"]'),
    ("elasticsearch", "elasticsearch", '["CMD-SHELL", "curl -sf http://localhost:9200/_cluster/health || exit 1"]'),
    ("rabbitmq", "rabbitmq", '["CMD", "rabbitmq-diagnostics", "check_running"]'),
    ("memcached", "memcached", '["CMD-SHELL", "echo stats | nc localhost 11211 | grep pid"]'),
    ("influxdb", "influxdb", '["CMD", "influx", "ping"]'),
]


def detect_healthcheck_pattern(service: dict) -> dict:
    """Detect the appropriate healthcheck pattern for a service.

    Returns a dict with: type, command, interval, timeout, retries, start_period.
    """
    image = service.get("image", "").lower()
    svc_name = service.get("name", "").lower()

    # Check against known service patterns
    for pattern, hc_type, hc_cmd in SERVICE_HEALTHCHECK_MAP:
        if pattern in image or pattern in svc_name:
            interval = "10s" if hc_type == "redis" else "30s"
            timeout = "5s" if hc_type == "redis" else "10s"
            start_period = "10s" if hc_type in ("redis", "mongo") else "30s"
            return {
                "type": hc_type,
                "command": hc_cmd,
                "interval": interval,
                "timeout": timeout,
                "retries": 5,
                "start_period": start_period,
            }

    # Default: web app with HTTP healthcheck
    # Use the first port if available
    ports = service.get("ports", [])
    port = ports[0]["container"] if ports else 8080
    return {
        "type": "web",
        "command": f'["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:{port}/"]',
        "interval": "30s",
        "timeout": "10s",
        "retries": 3,
        "start_period": "30s",
    }


# ---------------------------------------------------------------------------
# Subagent prompt generation
# ---------------------------------------------------------------------------

REQUIRED_README_SECTIONS = [
    "Quick Start",
    "Architecture",
    "Configuration",
    "Troubleshooting",
    "Backup/Recovery",
    "Links",
    "Prerequisites",
]


def generate_subagent_prompt(template: dict) -> str:
    """Generate a remediation prompt for a subagent to fix one template."""
    t_id = template["id"]
    t_name = template["name"]
    current_desc = template.get("current_description", "")
    derived_url = template.get("derived_project_url", "")
    services = template.get("compose_services", [])
    issues = template.get("issues", [])

    # Build issue summary
    issue_lines = []
    for issue in issues:
        issue_lines.append(f"- [{issue['severity']}] {issue['dimension']}: {issue['message']}")

    # Build service summary with healthcheck instructions
    service_lines = []
    for svc in services:
        hc = svc.get("healthcheck_pattern", {})
        hc_type = hc.get("type", "web")
        hc_cmd = hc.get("command", "")
        svc_lines = [
            f"  Service '{svc['name']}':",
            f"    Image: {svc.get('image', 'unknown')}",
            f"    Has healthcheck: {svc.get('has_healthcheck', False)}",
            f"    Has restart: {svc.get('has_restart', False)}",
            f"    Healthcheck type: {hc_type}",
            f"    Healthcheck command: {hc_cmd}",
        ]
        if hc:
            svc_lines.extend([
                f"    Interval: {hc.get('interval', '30s')}",
                f"    Timeout: {hc.get('timeout', '10s')}",
                f"    Retries: {hc.get('retries', 3)}",
                f"    Start period: {hc.get('start_period', '30s')}",
            ])
        service_lines.append("\n".join(svc_lines))

    prompt = f"""You are remediating the Arcane template '{t_id}' ({t_name}).

## Current State

Template directory: templates/{t_id}/

Current arcane.json description: "{current_desc}"

Derived project URL: {derived_url if derived_url else "Could not derive — use the template name to search for the project"}

Issues found by audit:
{chr(10).join(issue_lines) if issue_lines else "- No specific issues logged"}

Services in docker-compose.yml:
{chr(10).join(service_lines) if service_lines else "  No services detected"}

## Required Changes

### 1. Fix arcane.json description
- If the description contains "sourced from" markers, replace with a project-specific description
- Write 1-2 sentences describing what the application actually does
- If the derived project URL exists, reference the project's actual purpose from it
- Keep the existing id, name, version, author, tags fields unchanged

### 2. Fix docker-compose.yml
For each service that lacks a healthcheck, add one using the appropriate pattern:

**Web applications (HTTP):**
```yaml
healthcheck:
  test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:<port>/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Redis:**
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 10s
```

**PostgreSQL:**
```yaml
healthcheck:
  test: ["CMD", "pg_isready", "-U", "${{POSTGRES_USER:-app}}"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 30s
```

**MongoDB:**
```yaml
healthcheck:
  test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')", "--quiet"]
  interval: 10s
  timeout: 10s
  retries: 5
  start_period: 15s
```

**MySQL/MariaDB:**
```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 30s
```

For each service that lacks a restart policy, add:
```yaml
restart: unless-stopped
```

### 3. Rewrite README.md with 7+ sections
The README must include ALL of these sections (minimum 7):

1. **# {t_name}** — Brief project description (1-2 paragraphs, what it does, why you'd use it)
2. **## Quick Start** — Steps to deploy: cp .env.example .env, docker compose up -d, verify with curl, access URL
3. **## Architecture** — Table of components with descriptions, explain how services connect
4. **## Configuration** — Table of environment variables from .env.example with defaults and descriptions
5. **## Troubleshooting** — Common issues and solutions (port conflicts, permission errors, logs)
6. **## Backup/Recovery** — How to back up data volumes and restore from backup
7. **## Links** — Links to original project, documentation, Docker Hub/GHCR image, and community resources
8. **## Prerequisites** — Docker, Docker Compose version requirements, system resources

### Link to original project
{"If the derived URL is available, include it as the primary project link: " + derived_url if derived_url else "Search for the project using the template name and include a link to the original repository or homepage."}

## Output Format

After making changes, output:
1. The files you modified (list each path)
2. Any issues encountered
3. Whether each required change was completed (checklist)
"""
    return prompt


# ---------------------------------------------------------------------------
# Batch file generation
# ---------------------------------------------------------------------------

def load_and_filter_templates(audit_report_path: Path) -> list[dict]:
    """Load audit report and filter templates with documentation warnings."""
    if not audit_report_path.exists():
        logger.error("Audit report not found: %s", audit_report_path)
        sys.exit(1)

    with open(audit_report_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    templates = report.get("templates", [])
    logger.info("Loaded %d templates from audit report", len(templates))

    # Filter: templates with at least one warning in documentation dimension
    filtered = [
        t for t in templates
        if any(
            i["dimension"] == "documentation" and i["severity"] == "warning"
            for i in t.get("issues", [])
        )
    ]
    logger.info("Filtered to %d templates with documentation warnings", len(filtered))
    return filtered


def enrich_template(template: dict, templates_dir: Path) -> dict:
    """Enrich a template with compose services, healthcheck patterns, and current description."""
    t_id = template["id"]
    t_dir = templates_dir / t_id

    if not t_dir.is_dir():
        logger.warning("Template directory missing: %s — skipping", t_id)
        return None

    # Read arcane.json for current description
    arcane_path = t_dir / "arcane.json"
    current_description = ""
    if arcane_path.exists():
        try:
            with open(arcane_path, "r", encoding="utf-8") as f:
                arcane = json.load(f)
            current_description = arcane.get("description", "")
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Cannot read arcane.json for %s: %s", t_id, e)

    # Read and parse docker-compose.yml
    compose_path = t_dir / "docker-compose.yml"
    compose_services: list[dict] = []
    if compose_path.exists():
        try:
            compose_text = compose_path.read_text(encoding="utf-8")
            raw_services = _parse_compose_services(compose_text)
            # Enrich each service with healthcheck pattern
            for svc in raw_services:
                if not svc.get("has_healthcheck"):
                    svc["healthcheck_pattern"] = detect_healthcheck_pattern(svc)
                else:
                    svc["healthcheck_pattern"] = {"type": "existing", "command": "already defined"}
                compose_services.append(svc)
        except (OSError, UnicodeDecodeError) as e:
            logger.warning("Cannot read docker-compose.yml for %s: %s", t_id, e)

    # Derive project URL from first service's image
    derived_project_url = None
    if compose_services:
        first_image = compose_services[0].get("image", "")
        if first_image:
            derived_project_url, _ambiguous = _derive_project_url(first_image)

    # Build enriched template
    return {
        "id": t_id,
        "name": template.get("name", t_id),
        "issues": template.get("issues", []),
        "derived_project_url": derived_project_url,
        "compose_services": compose_services,
        "current_description": current_description,
    }


def generate_batches(
    templates: list[dict],
    templates_dir: Path,
    batch_size: int,
    wave: int,
) -> list[dict]:
    """Generate batch files from filtered templates.

    Returns list of batch dicts ready to write to JSON.
    """
    # Enrich templates
    enriched: list[dict] = []
    for t in templates:
        result = enrich_template(t, templates_dir)
        if result is not None:
            enriched.append(result)

    logger.info("Enriched %d templates (skipped %d missing dirs)",
                len(enriched), len(templates) - len(enriched))

    # Split into batches
    batches: list[dict] = []
    for i in range(0, len(enriched), batch_size):
        batch_templates = enriched[i:i + batch_size]
        batch_num = len(batches) + 1
        batch = {
            "batch_id": f"batch-{batch_num:02d}",
            "wave": wave,
            "template_count": len(batch_templates),
            "templates": batch_templates,
        }
        # Generate subagent prompt for each template
        for t in batch_templates:
            t["subagent_prompt"] = generate_subagent_prompt(t)
        batches.append(batch)

    logger.info("Generated %d batches (batch size %d)", len(batches), batch_size)
    return batches


def write_batches(batches: list[dict], batch_dir: Path) -> None:
    """Write batch files to disk."""
    batch_dir.mkdir(parents=True, exist_ok=True)
    for batch in batches:
        batch_id = batch["batch_id"]
        out_path = batch_dir / f"{batch_id}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)
        logger.info("Wrote %s (%d templates, %d bytes)",
                     out_path, batch["template_count"], out_path.stat().st_size)


def dry_run_report(batches: list[dict]) -> None:
    """Print batch plan without writing files."""
    total_templates = sum(b["template_count"] for b in batches)
    print(f"\n=== DRY RUN: Batch Plan ===")
    print(f"Total batches: {len(batches)}")
    print(f"Total templates: {total_templates}")
    print()
    for batch in batches:
        names = [t["name"] for t in batch["templates"]]
        print(f"  {batch['batch_id']}: {batch['template_count']} templates")
        for name in names:
            print(f"    - {name}")
    print(f"\nNo files written (--dry-run mode)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="M008 remediation wave — batch template remediation infrastructure",
    )
    parser.add_argument(
        "--audit-report",
        required=True,
        help="Path to audit-report.json from S01",
    )
    parser.add_argument(
        "--batch-dir",
        required=True,
        help="Directory to write batch JSON files",
    )
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Path to templates directory (default: templates/)",
    )
    parser.add_argument(
        "--wave",
        type=int,
        default=1,
        help="Wave number (default: 1)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Templates per batch (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print batch plan without writing files",
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

    audit_report_path = Path(args.audit_report)
    templates_dir = Path(args.templates_dir)
    batch_dir = Path(args.batch_dir)

    # Load and filter
    filtered = load_and_filter_templates(audit_report_path)

    if not filtered:
        logger.info("No templates with documentation warnings — nothing to do")
        return

    # Generate batches
    batches = generate_batches(filtered, templates_dir, args.batch_size, args.wave)

    if not batches:
        logger.warning("No batches generated (all templates skipped)")
        return

    # Output
    if args.dry_run:
        dry_run_report(batches)
    else:
        write_batches(batches, batch_dir)
        total = sum(b["template_count"] for b in batches)
        logger.info("Done: %d batches written, %d templates total", len(batches), total)


if __name__ == "__main__":
    main()
