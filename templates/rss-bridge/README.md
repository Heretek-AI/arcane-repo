# rss-bridge -- Self-Hosted Application

rss-bridge is a self-hosted application available through the YunoHost catalog.

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the application:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `RSS_BRIDGE_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `rss-bridge` | `ghcr.io/rss-bridge/rss-bridge:latest` | 8080 | rss-bridge application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f rss-bridge
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull rss-bridge
docker compose up -d
```

## Source

- YunoHost catalog entry: `rss-bridge`
