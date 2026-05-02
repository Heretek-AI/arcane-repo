# prometheus -- Self-Hosted Application

prometheus is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:9090](http://localhost:9090) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `PROMETHEUS_PORT` | `9090` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `prometheus` | `docker.io/prom/prometheus:latest` | 9090 | prometheus application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f prometheus
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull prometheus
docker compose up -d
```

## Source

- Yunohost catalog entry: `prometheus`
