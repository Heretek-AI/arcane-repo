# ChangeDetection -- Self-Hosted Application

ChangeDetection is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:5000](http://localhost:5000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `CHANGEDETECTION_PORT` | `5000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `changedetection` | `docker.io/thib4ut/changedetection:latest` | 5000 | ChangeDetection application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f changedetection
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull changedetection
docker compose up -d
```

## Source

- Portainer catalog entry: `ChangeDetection`
