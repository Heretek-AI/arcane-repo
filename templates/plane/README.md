# Plane -- Self-Hosted Application

Plane is a self-hosted application available through the Portainer catalog.

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
| `PLANE_PORT` | `8000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `plane` | `docker.io/plane/plane:latest` | 8000 | Plane application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f plane
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull plane
docker compose up -d
```

## Source

- Portainer catalog entry: `Plane`
