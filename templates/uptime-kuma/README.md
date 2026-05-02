# uptime-kuma -- Self-Hosted Application

uptime-kuma is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:3001](http://localhost:3001) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `UPTIME_KUMA_PORT` | `3001` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `uptime-kuma` | `ghcr.io/louislam/uptime-kuma:latest` | 3001 | uptime-kuma application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f uptime-kuma
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull uptime-kuma
docker compose up -d
```

## Source

- Umbrel catalog entry: `uptime-kuma`
