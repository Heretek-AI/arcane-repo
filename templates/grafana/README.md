# Grafana -- Self-Hosted Application

Grafana is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `GRAFANA_PORT` | `3000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `grafana` | `docker.io/grafana/grafana:latest` | 3000 | Grafana application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f grafana
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull grafana
docker compose up -d
```

## Source

- Portainer catalog entry: `Grafana`
