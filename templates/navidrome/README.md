# Navidrome -- Self-Hosted Application

Navidrome is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:4533](http://localhost:4533) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `NAVIDROME_PORT` | `4533` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `navidrome` | `ghcr.io/navidrome/navidrome:latest` | 4533 | Navidrome application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f navidrome
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull navidrome
docker compose up -d
```

## Source

- Portainer catalog entry: `Navidrome`
