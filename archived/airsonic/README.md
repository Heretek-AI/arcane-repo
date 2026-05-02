# airsonic -- Self-Hosted Application

airsonic is a self-hosted application available through the YunoHost catalog.

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

   Open [http://localhost:4040](http://localhost:4040) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `AIRSONIC_PORT` | `4040` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `airsonic` | `docker.io/airsonic/airsonic:latest` | 4040 | airsonic application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f airsonic
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull airsonic
docker compose up -d
```

## Source

- YunoHost catalog entry: `airsonic`
