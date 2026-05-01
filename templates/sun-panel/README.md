# Sun Panel

[Sun Panel](https://hub.docker.com/r/hslr/sun-panel) — Self-hosted dashboard and startpage for organizing your apps, bookmarks, and widgets. Clean, customizable web panel for your homelab or server.

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
