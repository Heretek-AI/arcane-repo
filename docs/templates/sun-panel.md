---
title: "Sun Panel"
description: "Self-hosted dashboard and startpage — organize apps, bookmarks, and widgets in a clean, customizable web panel"
---

# Sun Panel

Self-hosted dashboard and startpage — organize apps, bookmarks, and widgets in a clean, customizable web panel

## Tags

<a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/web" class="tag-badge">web</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sun-panel/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sun-panel/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sun-panel/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sun-panel` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dc24d27955bfb5c5c4507948613d3fffbb34aa8bf5ccc8c0cd04308fc5dc05ba` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the dashboard:**

   Open [http://localhost:3002](http://localhost:3002).

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `SUN_PANEL_PORT` | `3002` | Host port for the web UI |

## Service Details

- **Dashboard** — Customizable startpage on port 3002
- **App Management** — Add and organize apps, bookmarks, and widgets
- **Customization** — Themes, icons, and layout options
- **Storage** — Configuration and data persisted in named volumes (`sun_panel_data`, `sun_panel_conf`)

## Upstream

- [Docker Hub](https://hub.docker.com/r/hslr/sun-panel)

