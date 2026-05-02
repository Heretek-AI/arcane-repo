# gonic -- Self-Hosted Application

gonic is a self-hosted application available through the Yunohost catalog.

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
| `GONIC_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `gonic` | `ghcr.io/sentriz/gonic:latest` | 8080 | gonic application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f gonic
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull gonic
docker compose up -d
```

## Source

- Yunohost catalog entry: `gonic`
