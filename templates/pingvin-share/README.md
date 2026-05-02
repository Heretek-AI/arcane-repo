# pingvin-share -- Self-Hosted Application

pingvin-share is a self-hosted application available through the Umbrel catalog.

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
| `PINGVIN_SHARE_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `pingvin-share` | `ghcr.io/stonith404/pingvin-share:latest` | 8080 | pingvin-share application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f pingvin-share
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull pingvin-share
docker compose up -d
```

## Source

- Umbrel catalog entry: `pingvin-share`
