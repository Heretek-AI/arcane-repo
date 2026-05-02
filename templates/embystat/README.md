# EmbyStat -- Self-Hosted Application

EmbyStat is a self-hosted application available through the Portainer catalog.

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
| `EMBYSTAT_PORT` | `8096` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `embystat` | `ghcr.io/linuxserver/embystat:latest` | 8096 | EmbyStat application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f embystat
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull embystat
docker compose up -d
```

## Source

- Portainer catalog entry: `EmbyStat`
