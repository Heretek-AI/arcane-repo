# Appsmith -- Self-Hosted Application

Appsmith is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:80](http://localhost:80) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `APPSMITH_PORT` | `80` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `appsmith` | `docker.io/bitnamicharts/appsmith:latest` | 80 | Appsmith application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f appsmith
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull appsmith
docker compose up -d
```

## Source

- Portainer catalog entry: `Appsmith`
