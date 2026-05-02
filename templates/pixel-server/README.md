# Pixel-server -- Self-Hosted Application

Pixel-server is a self-hosted application available through the Portainer catalog.

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
| `PIXEL_SERVER_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `pixel-server` | `docker.io/olegvorobyov90/pixel-server:latest` | 8080 | Pixel-server application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f pixel-server
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull pixel-server
docker compose up -d
```

## Source

- Portainer catalog entry: `Pixel-server`
