#!/usr/bin/env python3
"""
process-candidates.py - Direct template creation from fact-cards.json

Reads fact-cards.json and creates template directories directly for
reachable candidates. Unreachable candidates go to review-queue.json.

Supports multiple source catalogs (yunohost, portainer, umbrel, etc.)
via the --source flag. The script parameterizes catalog name in tags,
descriptions, README text, and footer attribution.

Usage:
    python3 scripts/process-candidates.py --source yunohost [--dry-run]
    python3 scripts/process-candidates.py --source portainer [--dry-run]
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime, timezone

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FACT_CARDS = os.path.join(ROOT_DIR, 'fact-cards.json')
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
DEFAULT_REVIEW_QUEUE = os.path.join(ROOT_DIR, 'review-queue.json')


def slugify(name):
    """Convert candidate name to kebab-case slug."""
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s or name.lower()


def port_var_name(slug):
    """Maps slug to env var port name like SLUG_PORT."""
    return slug.upper().replace('-', '_') + '_PORT'


def guess_default_port(image):
    """Guess default internal port based on image name."""
    image_lower = image.lower()
    known = {
        'portainer': 9000, 'homeassistant': 8123, 'nodered': 1880,
        'grocy': 80, 'ttrss': 80, 'wallabag': 80, 'jellyfin': 8096,
        'peertube': 9000, 'nextcloud': 80, 'roundcube': 80, 'phpbb': 80,
        'prometheus': 9090, 'grafana': 3000, 'elasticsearch': 9200,
        'influxdb': 8086, 'loki': 3100, 'synapse': 8008, 'matrix': 8008,
        'vaultwarden': 80, 'bitwarden': 80, 'gitea': 3000, 'gitlab': 80,
        'drone': 80, 'jenkins': 8080, 'woodpecker': 8000,
        'minio': 9000, 'seafile': 80, 'onlyoffice': 80,
        'mastodon': 3000, 'pleroma': 4000, 'pixelfed': 80,
        'funkwhale': 80, 'navidrome': 4533, 'airsonic': 4040,
        'transmission': 9091, 'deluge': 8112, 'qbittorrent': 8080,
        'plex': 32400, 'emby': 8096, 'calibre': 8083,
        'paperless': 8000, 'mayan': 8000, 'docspell': 7880,
        'firefly': 8080, 'actual': 5006, 'freshrss': 80,
        'changedetection': 5000, 'ntfy': 80, 'gotify': 80,
        'uptime': 3001, 'statping': 8080, 'cachet': 80,
        'librespeed': 80, 'speedtest': 80, 'it-tools': 80,
        'stirling': 8080, 'drawio': 8080, 'diagrams': 8080,
        'excalidraw': 80, 'hedgedoc': 3000, 'codimd': 3000,
        'outline': 3000, 'bookstack': 8080, 'wiki': 80,
        'dokuwiki': 80, 'mediawiki': 80, 'confluence': 8090,
        'wekan': 8080, 'taiga': 80, 'plane': 8000, 'focalboard': 8000,
        'nocodb': 8080, 'baserow': 80, 'directus': 8055, 'strapi': 1337,
        'n8n': 5678, 'nodered': 1880, 'appsmith': 80,
        'langflow': 7860, 'flowise': 3000, 'dify': 3000,
        'openwebui': 3000, 'chatbot': 3000, 'ollama': 11434,
        'anythingllm': 3001, 'localai': 8080,
        '2fauth': 8000, 'authelia': 9091, 'authentik': 9000,
        'keycloak': 8080, 'zitadel': 8080, 'casdoor': 8000,
    }
    for key, port in known.items():
        if key in image_lower:
            return port
    return 8080


def extract_tags(candidate_name, hints, source_name):
    """Generate relevant tags from candidate data."""
    tags = ['self-hosted']
    name_lower = candidate_name.lower()
    ai_kw = ['ai', 'llm', 'gpt', 'chatgpt', 'agent', 'ml', 'neural', 'inference', 'copilot', 'langchain']
    cms_kw = ['cms', 'wiki', 'blog', 'docs', 'static', 'content']
    mon_kw = ['monitor', 'metrics', 'dashboard', 'grafana', 'prometheus', 'alert', 'observ']
    sto_kw = ['storage', 'file', 'sync', 'drive', 'backup', 's3']
    com_kw = ['chat', 'messag', 'matrix', 'email', 'mail', 'irc', 'xmpp']
    dev_kw = ['ci', 'cd', 'deploy', 'git', 'docker', 'k8s', 'kubernetes']
    if any(kw in name_lower for kw in ai_kw): tags.append('ai')
    if any(kw in name_lower for kw in cms_kw): tags.append('cms')
    if any(kw in name_lower for kw in mon_kw): tags.append('monitoring')
    if any(kw in name_lower for kw in sto_kw): tags.append('storage')
    if any(kw in name_lower for kw in com_kw): tags.append('communication')
    if any(kw in name_lower for kw in dev_kw): tags.append('devops')
    source_tag = '%s-source' % source_name
    if source_tag in hints:
        tags.append(source_name)
    return tags[:4]


def create_arcane_json(slug, data, source_name):
    """Build arcane.json per template-builder agent contract."""
    name = data.get('candidate', slug)
    tags = extract_tags(name, data.get('classification_hints', []), source_name)
    title = name.replace('-', ' ').replace('_', ' ').title()
    source_title = source_name.title()
    return {
        "id": slug,
        "name": title,
        "description": "Self-hosted %s deployment via Docker, sourced from %s catalog" % (title, source_title),
        "version": "1.0.0",
        "author": "Arcane",
        "tags": tags
    }


def create_docker_compose(slug, data):
    """Build docker-compose.yml per Docker-Ready pattern (M004)."""
    image = data.get('recommend_image', '')
    if not image:
        return ''
    port_var = port_var_name(slug)
    default_port = guess_default_port(image)
    host_port = "${%s:-%d}" % (port_var, default_port)
    
    lines = []
    lines.append("version: '3.8'")
    lines.append("")
    lines.append("services:")
    lines.append("  %s:" % slug)
    lines.append("    image: %s" % image)
    lines.append("    container_name: %s" % slug)
    lines.append("    hostname: %s" % slug)
    lines.append("    ports:")
    lines.append("      - \"%s:%d\"" % (host_port, default_port))
    lines.append("    volumes:")
    lines.append("      - %s_data:/data" % slug)
    lines.append("    restart: unless-stopped")
    lines.append("")
    lines.append("volumes:")
    lines.append("  %s_data:" % slug)
    lines.append("    name: %s_data" % slug)
    return '\n'.join(lines) + '\n'


def create_env_example(slug, data):
    """Build .env.example per Docker-Ready pattern."""
    name = data.get('candidate', slug)
    port_var = port_var_name(slug)
    default_port = guess_default_port(data.get('recommend_image', ''))
    
    lines = []
    lines.append("# -- %s Configuration --" % name)
    lines.append("# Copy this file to .env and adjust values as needed.")
    lines.append("")
    lines.append("# -- Port --")
    lines.append("# %s host port (default: %d)" % (name, default_port))
    lines.append("%s=%d" % (port_var, default_port))
    return '\n'.join(lines) + '\n'


def create_readme(slug, data, source_name):
    """Build README.md per Docker-Ready pattern."""
    name = data.get('candidate', slug)
    port_var = port_var_name(slug)
    default_port = guess_default_port(data.get('recommend_image', ''))
    github_url = data.get('github_url', '')
    image = data.get('recommend_image', '')
    source_title = source_name.title()
    
    lines = []
    lines.append("# %s -- Self-Hosted Application" % name)
    lines.append("")
    if github_url:
        lines.append("[%s](%s) is a self-hosted application available through the %s catalog." % (name, github_url, source_title))
    else:
        lines.append("%s is a self-hosted application available through the %s catalog." % (name, source_title))
    lines.append("")
    lines.append("## Quick Start")
    lines.append("")
    lines.append("1. **Copy and edit the environment file:**")
    lines.append("")
    lines.append("   ```bash")
    lines.append("   cp .env.example .env")
    lines.append("   ```")
    lines.append("")
    lines.append("2. **Start the service:**")
    lines.append("")
    lines.append("   ```bash")
    lines.append("   docker compose up -d")
    lines.append("   ```")
    lines.append("")
    lines.append("3. **Access the application:**")
    lines.append("")
    lines.append("   Open [http://localhost:%d](http://localhost:%d) in your browser." % (default_port, default_port))
    lines.append("")
    lines.append("## Configuration")
    lines.append("")
    lines.append("Copy `.env.example` to `.env` and edit:")
    lines.append("")
    lines.append("| Variable | Default | Description |")
    lines.append("|----------|---------|-------------|")
    lines.append("| `%s` | `%d` | Host port for the service |" % (port_var, default_port))
    lines.append("")
    lines.append("## Services")
    lines.append("")
    lines.append("| Service | Image | Port | Description |")
    lines.append("|---------|-------|------|-------------|")
    lines.append("| `%s` | `%s` | %d | %s application |" % (slug, image, default_port, name))
    lines.append("")
    lines.append("## Managing the Service")
    lines.append("")
    lines.append("**View logs:**")
    lines.append("")
    lines.append("```bash")
    lines.append("docker compose logs -f %s" % slug)
    lines.append("```")
    lines.append("")
    lines.append("**Stop the service:**")
    lines.append("")
    lines.append("```bash")
    lines.append("docker compose down")
    lines.append("```")
    lines.append("")
    lines.append("**Update to the latest version:**")
    lines.append("")
    lines.append("```bash")
    lines.append("docker compose pull %s" % slug)
    lines.append("docker compose up -d")
    lines.append("```")
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append("- %s catalog entry: `%s`" % (source_title, name))
    if github_url:
        lines.append("- Upstream project: %s" % github_url)
    
    return '\n'.join(lines) + '\n'


def create_template(slug, data, source_name, dry_run=False):
    """Create template directory with all 4 required files."""
    template_dir = os.path.join(TEMPLATES_DIR, slug)
    img = data.get('recommend_image', '')[:50]
    
    if os.path.exists(template_dir):
        print("  [SKIP] %s: directory already exists" % slug)
        return False
    
    if dry_run:
        print("  [DRY-RUN] %s: would create template (image: %s)" % (slug, img))
        return True
    
    os.makedirs(template_dir, exist_ok=True)
    
    # arcane.json
    arcane = create_arcane_json(slug, data, source_name)
    with open(os.path.join(template_dir, 'arcane.json'), 'w', encoding='utf-8') as f:
        json.dump(arcane, f, indent=2)
        f.write('\n')
    
    # docker-compose.yml
    dc = create_docker_compose(slug, data)
    with open(os.path.join(template_dir, 'docker-compose.yml'), 'w', encoding='utf-8') as f:
        f.write(dc)
    
    # .env.example
    env = create_env_example(slug, data)
    with open(os.path.join(template_dir, '.env.example'), 'w', encoding='utf-8') as f:
        f.write(env)
    
    # README.md
    readme = create_readme(slug, data, source_name)
    with open(os.path.join(template_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("  [OK] %s: created template (image: %s)" % (slug, img))
    return True


def build_review_entry(candidate, source_name):
    """Build review-queue entry for unreachable candidate."""
    name = candidate.get('candidate', 'unknown')
    images = candidate.get('images_checked', [])
    hints = candidate.get('classification_hints', [])
    
    reasons = ["no reachable Docker image found across Docker Hub library, Docker Hub org, and GHCR"]
    
    hypothesis = "needs-investigation"
    if 'needs-investigation' in hints:
        hypothesis = "needs-investigation"
    if 'system-exclusion' in hints:
        hypothesis = "system-exclusion"
    
    return {
        "candidate": name,
        "source": candidate.get('source', source_name),
        "ambiguity": "; ".join(reasons),
        "hypothesis": hypothesis,
        "recommendation": "Manual review: check if Docker image exists under different name or requires custom-build",
        "agent": "template-builder",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def main():
    parser = argparse.ArgumentParser(
        description='Process fact-cards.json into template directories and review-queue entries.')
    parser.add_argument('--source', required=True,
                        help='Source catalog name (e.g. yunohost, portainer, umbrel)')
    parser.add_argument('--input', default=DEFAULT_FACT_CARDS,
                        help='Path to fact-cards.json (default: fact-cards.json)')
    parser.add_argument('--output', default=DEFAULT_REVIEW_QUEUE,
                        help='Path to review-queue.json output (default: review-queue.json)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Simulate without writing files')
    args = parser.parse_args()
    
    source_name = args.source.lower()
    fact_cards_path = args.input
    review_queue_path = args.output
    
    if not os.path.exists(fact_cards_path):
        print("ERROR: fact-cards.json not found at %s" % fact_cards_path, file=sys.stderr)
        sys.exit(1)
    
    with open(fact_cards_path, 'r', encoding='utf-8') as f:
        fact_cards = json.load(f)
    
    print("Loaded %d fact cards (source: %s)" % (len(fact_cards), source_name))
    
    reachable = [c for c in fact_cards if c.get('recommend_image')]
    unreachable = [c for c in fact_cards if not c.get('recommend_image')]
    
    print("Reachable: %d" % len(reachable))
    print("Unreachable: %d" % len(unreachable))
    
    created = 0
    skipped = 0
    
    print("\n--- Creating templates for %d reachable candidates ---" % len(reachable))
    for candidate in reachable:
        name = candidate.get('candidate', '')
        slug = slugify(name)
        if create_template(slug, candidate, source_name, args.dry_run):
            created += 1
        else:
            skipped += 1
    
    print("\n--- Building review-queue for %d unreachable candidates ---" % len(unreachable))
    review_entries = []
    for candidate in unreachable:
        review_entries.append(build_review_entry(candidate, source_name))
    
    if not args.dry_run:
        with open(review_queue_path, 'w', encoding='utf-8') as f:
            json.dump(review_entries, f, indent=2)
            f.write('\n')
        print("Wrote %d entries to %s" % (len(review_entries), os.path.basename(review_queue_path)))
    else:
        print("[DRY-RUN] Would write %d entries to %s" % (len(review_entries), os.path.basename(review_queue_path)))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("  Source: %s" % source_name)
    print("  Templates created: %d" % created)
    print("  Templates skipped (already exist): %d" % skipped)
    print("  Review queue entries: %d" % len(review_entries))
    if not args.dry_run:
        existing = len([d for d in os.listdir(TEMPLATES_DIR) if os.path.isdir(os.path.join(TEMPLATES_DIR, d))])
        print("  Total templates in registry: %d" % existing)
    print("=" * 60)
    
    if args.dry_run:
        print("\nDRY RUN - no files written. Remove --dry-run to execute.")

if __name__ == '__main__':
    main()
