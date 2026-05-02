# Paperless NGX -- Self-Hosted Application

Paperless NGX is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `PAPERLESS_NGX_PORT` | `8000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `paperless-ngx` | `ghcr.io/paperless-ngx/paperless-ngx:latest` | 8000 | Paperless NGX application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f paperless-ngx
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull paperless-ngx
docker compose up -d
```

## Source

- Portainer catalog entry: `Paperless NGX`
