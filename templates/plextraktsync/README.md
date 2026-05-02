# PlexTraktSync -- Self-Hosted Application

PlexTraktSync is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:32400](http://localhost:32400) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `PLEXTRAKTSYNC_PORT` | `32400` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `plextraktsync` | `docker.io/p2bauer/plextraktsync:latest` | 32400 | PlexTraktSync application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f plextraktsync
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull plextraktsync
docker compose up -d
```

## Source

- Portainer catalog entry: `PlexTraktSync`
