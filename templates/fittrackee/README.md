# fittrackee -- Self-Hosted Application

fittrackee is a self-hosted application available through the YunoHost catalog.

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
| `FITTRACKEE_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `fittrackee` | `docker.io/fittrackee/fittrackee:latest` | 8080 | fittrackee application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f fittrackee
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull fittrackee
docker compose up -d
```

## Source

- YunoHost catalog entry: `fittrackee`
