# Jellyfin -- Self-Hosted Application

Jellyfin is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:8096](http://localhost:8096) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `JELLYFIN_PORT` | `8096` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `jellyfin` | `ghcr.io/jellyfin/jellyfin:latest` | 8096 | Jellyfin application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f jellyfin
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull jellyfin
docker compose up -d
```

## Source

- Portainer catalog entry: `Jellyfin`
