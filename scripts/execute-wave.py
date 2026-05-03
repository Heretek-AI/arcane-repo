#!/usr/bin/env python3
"""
Remediation wave executor for M008/S02.

Processes batch files and remediates templates:
1. Fixes arcane.json descriptions (removes "sourced from" markers)
2. Adds healthchecks to docker-compose.yml services
3. Adds restart policies to docker-compose.yml services
4. Rewrites README.md with 7+ sections of project-specific content

Uses stdlib only. Reads batch JSON files produced by remediate-wave.py.
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Healthcheck patterns by service type
HEALTHCHECK_PATTERNS: dict[str, dict[str, Any]] = {
    "web": {
        "command": '["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/"]',
        "interval": "30s",
        "timeout": "10s",
        "retries": 3,
        "start_period": "30s",
    },
    "redis": {
        "command": '["CMD", "redis-cli", "ping"]',
        "interval": "10s",
        "timeout": "5s",
        "retries": 5,
        "start_period": "10s",
    },
    "postgres": {
        "command": '["CMD", "pg_isready", "-U", "${POSTGRES_USER:-app}"]',
        "interval": "30s",
        "timeout": "10s",
        "retries": 5,
        "start_period": "30s",
    },
    "mongo": {
        "command": '["CMD", "mongosh", "--eval", "db.adminCommand(\'ping\')", "--quiet"]',
        "interval": "10s",
        "timeout": "10s",
        "retries": 5,
        "start_period": "15s",
    },
    "mysql": {
        "command": '["CMD", "mysqladmin", "ping", "-h", "localhost"]',
        "interval": "30s",
        "timeout": "10s",
        "retries": 5,
        "start_period": "30s",
    },
}

# Patterns for "sourced from" descriptions
SOURCED_FROM_PATTERNS = [
    r"\s*[—–-]\s*sourced from\s+[\w-]+\s+catalog",
    r",?\s*sourced from\s+[\w-]+\s+catalog",
    r"\s*via Docker\s*[—–-]?\s*sourced from\s+[\w-]+\s+catalog",
    r"Self-hosted\s+[\w-]+\s+deployment via Docker,?\s*sourced from\s+[\w-]+\s+catalog",
    r"Self-hosted\s+[\w-]+\s+deployment via Docker\s*[—–-]\s*sourced from\s+[\w-]+\s+catalog",
]


def detect_service_type(image: str, service_name: str) -> str:
    """Detect service type from image name for healthcheck pattern selection."""
    image_lower = image.lower()
    name_lower = service_name.lower()

    if any(x in image_lower for x in ["redis"]):
        return "redis"
    if any(x in image_lower for x in ["postgres", "pgvector", "postgis"]):
        return "postgres"
    if any(x in image_lower for x in ["mongo"]):
        return "mongo"
    if any(x in image_lower for x in ["mysql", "mariadb"]):
        return "mysql"
    # Default to web for application containers
    return "web"


def fix_arcane_description(description: str, template_name: str, derived_url: str | None) -> str:
    """Remove 'sourced from' markers and generate a project-specific description."""
    # Check if description actually needs fixing
    has_sourced = any(
        re.search(pattern, description, re.IGNORECASE)
        for pattern in SOURCED_FROM_PATTERNS
    )

    if has_sourced:
        # Extract the core description before "sourced from"
        cleaned = description
        for pattern in SOURCED_FROM_PATTERNS:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()

        # If the cleaned description is too generic or empty, generate a new one
        if len(cleaned) < 20 or "deployment via Docker" in cleaned.lower():
            cleaned = f"Self-hosted {template_name} deployment for containerized environments"

        # Clean up trailing punctuation and whitespace
        cleaned = cleaned.rstrip(".,;:").strip()

        return cleaned

    return description  # No change needed


def derive_description(template: dict) -> str:
    """Generate a meaningful description for a template based on available info."""
    name = template["name"]
    url = template.get("derived_project_url")
    current = template.get("current_description", "")

    # If description is already good (no "sourced from", decent length), keep it
    has_sourced = any(
        re.search(p, current, re.IGNORECASE)
        for p in SOURCED_FROM_PATTERNS
    )

    if not has_sourced and len(current) > 30:
        return current

    # Clean up the description
    cleaned = fix_arcane_description(current, name, url)
    if len(cleaned) > 30 and "sourced from" not in cleaned.lower():
        return cleaned

    # Fallback: generate from template name
    return f"Self-hosted {name} deployment for containerized environments"


def _is_top_level_key(line: str) -> bool:
    """Check if a line is a top-level compose key (services, volumes, networks, etc.)."""
    return bool(re.match(r"^\w", line)) and ":" in line


def _parse_compose_services(compose_content: str) -> list[dict]:
    """Parse compose content and return service boundaries with start/end line indices."""
    lines = compose_content.split("\n")
    services = []
    in_services_block = False
    current_svc = None

    for i, line in enumerate(lines):
        # Detect top-level 'services:' key
        if re.match(r"^services:\s*$", line) or re.match(r"^services:\s*#", line):
            in_services_block = True
            continue

        # Detect other top-level keys (exit services block)
        if re.match(r"^\w", line) and ":" in line and not line.startswith(" "):
            if line.strip().startswith("services"):
                in_services_block = True
            else:
                in_services_block = False
                if current_svc:
                    current_svc["end"] = i
                    services.append(current_svc)
                    current_svc = None
            continue

        # Inside services block, detect service definitions (2-space indent)
        if in_services_block:
            svc_match = re.match(r"^  (\w[\w-]*):", line)
            if svc_match:
                if current_svc:
                    current_svc["end"] = i
                    services.append(current_svc)
                current_svc = {
                    "name": svc_match.group(1),
                    "start": i,
                    "end": len(lines),  # Will be updated
                }

    # Close last service
    if current_svc:
        current_svc["end"] = len(lines)
        services.append(current_svc)

    return services


def _insert_before_line(lines: list[str], insert_idx: int, block: str) -> list[str]:
    """Insert a block of text before a given line index."""
    return lines[:insert_idx] + [block] + lines[insert_idx:]


def add_healthcheck_to_compose(
    compose_content: str,
    service_name: str,
    service_type: str,
    port: int = 8080,
) -> str:
    """Add healthcheck to a service in docker-compose.yml content."""
    pattern = HEALTHCHECK_PATTERNS.get(service_type, HEALTHCHECK_PATTERNS["web"])

    # Build the healthcheck YAML block
    cmd = pattern["command"].replace("8080", str(port))
    healthcheck_block = (
        f"    healthcheck:\n"
        f'      test: {cmd}\n'
        f"      interval: {pattern['interval']}\n"
        f"      timeout: {pattern['timeout']}\n"
        f"      retries: {pattern['retries']}\n"
        f"      start_period: {pattern['start_period']}"
    )

    lines = compose_content.split("\n")
    services = _parse_compose_services(compose_content)

    # Find the target service
    target = None
    for svc in services:
        if svc["name"] == service_name:
            target = svc
            break

    if target is None:
        return compose_content  # Service not found

    # Check if service already has healthcheck
    svc_lines = lines[target["start"]:target["end"]]
    has_healthcheck = any("healthcheck:" in line for line in svc_lines)

    if has_healthcheck:
        return compose_content

    # Find the last line of the service (before next service or end of services block)
    # Insert healthcheck before the service's end boundary
    insert_idx = target["end"]

    # Trim trailing blank lines within the service
    while insert_idx > target["start"] and lines[insert_idx - 1].strip() == "":
        insert_idx -= 1

    # Insert after the last non-blank line of the service
    lines = lines[:insert_idx] + [healthcheck_block] + lines[insert_idx:]
    return "\n".join(lines)


def add_restart_policy(compose_content: str, service_name: str) -> str:
    """Add restart: unless-stopped to a service if missing."""
    lines = compose_content.split("\n")
    services = _parse_compose_services(compose_content)

    # Find the target service
    target = None
    for svc in services:
        if svc["name"] == service_name:
            target = svc
            break

    if target is None:
        return compose_content

    # Check if service already has restart policy
    svc_lines = lines[target["start"]:target["end"]]
    has_restart = any(re.search(r"restart:", line) for line in svc_lines)

    if has_restart:
        return compose_content

    # Find insertion point (last non-blank line of the service)
    insert_idx = target["end"]
    while insert_idx > target["start"] and lines[insert_idx - 1].strip() == "":
        insert_idx -= 1

    lines = lines[:insert_idx] + ["    restart: unless-stopped"] + lines[insert_idx:]
    return "\n".join(lines)


def extract_port_from_compose(compose_content: str, service_name: str) -> int:
    """Try to extract the first exposed port from a compose service."""
    lines = compose_content.split("\n")
    in_service = False

    for line in lines:
        if re.match(rf"^\s{{2}}{re.escape(service_name)}:", line):
            in_service = True
            continue
        if in_service and re.match(r"^\s{2}\w", line) and ":" in line:
            break  # Next service
        if in_service:
            # Look for port mapping like "8080:8080" or "${PORT:-8080}:8080"
            port_match = re.search(r'"?\$\{?\w*(?::?-?(\d+))\}?:(\d+)"?', line)
            if port_match:
                return int(port_match.group(2) or port_match.group(1))
            # Simple port mapping
            port_match = re.search(r'"?(\d+):(\d+)"?', line)
            if port_match:
                return int(port_match.group(2))

    return 8080  # Default


def generate_readme(template: dict, compose_content: str, arcane_content: str) -> str:
    """Generate a comprehensive README with 7+ sections."""
    name = template["name"]
    slug = template["id"]
    url = template.get("derived_project_url", "")
    description = derive_description(template)

    # Parse services from compose
    services = []
    current_service = None
    for line in compose_content.split("\n"):
        svc_match = re.match(r"^\s{2}(\w[\w-]*):", line)
        if svc_match:
            svc_name = svc_match.group(1)
            if svc_name != "volumes" and svc_name != "networks":
                current_service = svc_name
                services.append({"name": svc_name, "image": ""})
        if current_service:
            img_match = re.match(r'\s+image:\s*(.+)', line)
            if img_match:
                services[-1]["image"] = img_match.group(1).strip()

    # Filter out data/init services for architecture description
    app_services = [s for s in services if not s["name"].endswith("_data") and not s["name"].endswith("_init")]
    data_services = [s for s in services if s["name"].endswith("_data")]

    # Build architecture table
    arch_rows = ""
    for svc in app_services:
        img = svc["image"] or "embedded"
        arch_rows += f"| `{svc['name']}` | {img} | Main application service |\n"
    for svc in data_services:
        arch_rows += f"| `{svc['name']}` | (volume) | Persistent data storage |\n"

    # Determine primary port
    primary_port = extract_port_from_compose(compose_content, app_services[0]["name"] if app_services else slug)

    # Check for .env.example
    env_section = ""
    env_path = Path(f"templates/{slug}/.env.example")
    if env_path.exists():
        env_content = env_path.read_text()
        env_rows = ""
        for eline in env_content.split("\n"):
            if "=" in eline and not eline.strip().startswith("#"):
                var_name = eline.split("=")[0].strip()
                default_val = eline.split("=", 1)[1].strip() if "=" in eline else ""
                env_rows += f"| `{var_name}` | `{default_val}` | Configuration variable |\n"
        if env_rows:
            env_section = f"""## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
{env_rows}"""

    # Build the README
    link_section = ""
    if url:
        link_section += f"- **Project Homepage:** [{name}]({url})\n"
    link_section += f"- **Docker Image:** `{app_services[0]['image'] if app_services else slug}`\n"
    if url:
        link_section += f"- **Documentation:** [GitHub Wiki]({url}/wiki)\n"
        link_section += f"- **Issues:** [GitHub Issues]({url}/issues)\n"

    readme = f"""# {name}

{description}

This template provides a containerized deployment of [{name}]({"https://github.com/" + url.split("github.com/")[-1] if url and "github.com" in url else url or name.lower()}) using Docker Compose.

## Quick Start

1. **Clone and configure:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Verify it's running:**

   ```bash
   docker compose ps
   curl -s http://localhost:{primary_port}/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:{primary_port}](http://localhost:{primary_port}) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
{arch_rows}
Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

{env_section if env_section else f"""Configure the deployment by editing `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `{slug.upper()}_PORT` | `{primary_port}` | Host port for the web interface |
"""}

## Troubleshooting

**Container won't start:**
```bash
docker compose logs {app_services[0]['name'] if app_services else slug}
```

**Port conflict:**
Edit `.env` and change `{slug.upper()}_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec {app_services[0]['name'] if app_services else slug} ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect {slug} --format='{{{{json .State.Health}}}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v {slug}_data:/data -v $(pwd):/backup alpine tar czf /backup/{slug}-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v {slug}_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/{slug}-backup.tar.gz -C /"
docker compose up -d
```

## Links

{link_section}

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
"""

    return readme


def process_template(
    template: dict,
    templates_dir: Path,
    dry_run: bool = False,
) -> dict:
    """Process a single template: fix arcane.json, compose, and README."""
    slug = template["id"]
    template_dir = templates_dir / slug
    result = {
        "id": slug,
        "name": template["name"],
        "status": "success",
        "files_modified": [],
        "errors": [],
    }

    if not template_dir.exists():
        result["status"] = "skipped"
        result["errors"].append(f"Template directory not found: {template_dir}")
        return result

    try:
        # 1. Fix arcane.json
        arcane_path = template_dir / "arcane.json"
        if arcane_path.exists():
            arcane = json.loads(arcane_path.read_text(encoding="utf-8"))
            old_desc = arcane.get("description", "")
            new_desc = derive_description(template)

            if old_desc != new_desc:
                arcane["description"] = new_desc
                if not dry_run:
                    arcane_path.write_text(
                        json.dumps(arcane, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8",
                    )
                result["files_modified"].append("arcane.json")

        # 2. Fix docker-compose.yml
        compose_path = template_dir / "docker-compose.yml"
        if compose_path.exists():
            compose_content = compose_path.read_text(encoding="utf-8")
            original_compose = compose_content

            # Process each service
            for svc in template.get("compose_services", []):
                svc_name = svc["name"]
                image = svc.get("image", "")

                # Add healthcheck if missing
                if not svc.get("has_healthcheck", False):
                    svc_type = detect_service_type(image, svc_name)
                    port = extract_port_from_compose(compose_content, svc_name)
                    compose_content = add_healthcheck_to_compose(
                        compose_content, svc_name, svc_type, port
                    )

                # Add restart policy if missing
                if not svc.get("has_restart", False):
                    compose_content = add_restart_policy(compose_content, svc_name)

            if compose_content != original_compose:
                if not dry_run:
                    compose_path.write_text(compose_content, encoding="utf-8")
                result["files_modified"].append("docker-compose.yml")

        # 3. Rewrite README
        readme_path = template_dir / "README.md"
        if readme_path.exists():
            compose_for_readme = compose_path.read_text(encoding="utf-8") if compose_path.exists() else ""
            arcane_for_readme = arcane_path.read_text(encoding="utf-8") if arcane_path.exists() else ""

            new_readme = generate_readme(template, compose_for_readme, arcane_for_readme)

            if not dry_run:
                readme_path.write_text(new_readme, encoding="utf-8")
            result["files_modified"].append("README.md")

    except Exception as e:
        result["status"] = "failed"
        result["errors"].append(str(e))
        log.error(f"Failed to process {slug}: {e}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Remediation wave executor")
    parser.add_argument(
        "--batch-dir",
        default=".gsd/milestones/M008/slices/S02/batches",
        help="Directory containing batch JSON files",
    )
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Directory containing template directories",
    )
    parser.add_argument(
        "--wave",
        type=int,
        default=1,
        help="Wave number (determines batch range: wave 1 = batches 1-8, wave 2 = 9-16, etc.)",
    )
    parser.add_argument(
        "--batches-per-wave",
        type=int,
        default=8,
        help="Number of batches per wave",
    )
    parser.add_argument(
        "--output",
        help="Output results file path (default: wave{N}-results.json in batch dir parent)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write files, just report what would change",
    )
    parser.add_argument(
        "--specific-batch",
        help="Process only a specific batch file (e.g., batch-01.json)",
    )
    args = parser.parse_args()

    batch_dir = Path(args.batch_dir)
    templates_dir = Path(args.templates_dir)

    if not batch_dir.exists():
        log.error(f"Batch directory not found: {batch_dir}")
        sys.exit(1)

    # Determine which batches to process
    if args.specific_batch:
        batch_files = [batch_dir / args.specific_batch]
    else:
        start = (args.wave - 1) * args.batches_per_wave + 1
        end = start + args.batches_per_wave
        batch_files = [
            batch_dir / f"batch-{i:02d}.json"
            for i in range(start, end)
        ]

    # Load all templates from batch files
    all_templates = []
    for bf in batch_files:
        if not bf.exists():
            log.warning(f"Batch file not found, skipping: {bf}")
            continue
        batch = json.loads(bf.read_text(encoding="utf-8"))
        templates = batch.get("templates", [])
        log.info(f"Loaded {bf.name}: {len(templates)} templates")
        all_templates.extend(templates)

    if not all_templates:
        log.error("No templates found in batch files")
        sys.exit(1)

    log.info(f"Processing {len(all_templates)} templates (wave {args.wave})")

    # Process each template
    results = []
    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, template in enumerate(all_templates, 1):
        slug = template["id"]
        log.info(f"[{i}/{len(all_templates)}] Processing {slug}...")

        result = process_template(template, templates_dir, dry_run=args.dry_run)
        results.append(result)

        if result["status"] == "success":
            success_count += 1
            log.info(f"  ✓ {slug}: modified {', '.join(result['files_modified'])}")
        elif result["status"] == "skipped":
            skip_count += 1
            log.warning(f"  ⊘ {slug}: skipped — {result['errors']}")
        else:
            fail_count += 1
            log.error(f"  ✗ {slug}: failed — {result['errors']}")

    # Write results
    wave_results = {
        "wave": args.wave,
        "batch_range": f"batch-{((args.wave - 1) * args.batches_per_wave + 1):02d} to batch-{(args.wave * args.batches_per_wave):02d}",
        "total_processed": len(all_templates),
        "summary": {
            "success": success_count,
            "failed": fail_count,
            "skipped": skip_count,
        },
        "templates": results,
    }

    output_path = args.output or str(
        batch_dir.parent / f"wave{args.wave}-results.json"
    )

    if not args.dry_run:
        Path(output_path).write_text(
            json.dumps(wave_results, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        log.info(f"Results written to {output_path}")
    else:
        log.info(f"[DRY RUN] Would write results to {output_path}")

    # Print summary
    log.info(f"\n{'='*50}")
    log.info(f"Wave {args.wave} Summary:")
    log.info(f"  Total: {len(all_templates)}")
    log.info(f"  Success: {success_count}")
    log.info(f"  Failed: {fail_count}")
    log.info(f"  Skipped: {skip_count}")
    log.info(f"{'='*50}")

    if fail_count > 0:
        log.warning("Some templates failed — check results for details")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
