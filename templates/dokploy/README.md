# Dokploy

Self-hosted deployment platform

## Project Overview

[Dokploy](https://github.com/Dokploy/dokploy) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run Dokploy in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `dokploy` | `dokploy/dokploy:latest` | Main application service |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `dokploy_data` | (varies) | Persistent data storage |

### Networks

Uses the default Docker bridge network. If you need to connect to other services (databases, APIs, reverse proxy), attach it to a shared Docker network.

## Quick Start

### 1. Configure environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start the service

```bash
docker compose up -d
```

### 3. Verify it's running

```bash
docker compose ps
curl -s http://localhost:3000/ | head -c 200
```

### 4. Access the application

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration Reference

### Environment Variables

Set these in your `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DOKPLOY_PORT` | `3000` | Host port for Dokploy web dashboard (default: 3000) |
| `DOKPLOY_NODE_ENV` | `production` | Node.js environment mode: production, development |
| `DOKPLOY_SECRET_KEY` | `—` | Secret key for session encryption (generate a random string) |


## Troubleshooting

### Container won't start

Check the logs for error messages:

```bash
docker compose logs
```

### Port conflict

If the default port 3000 is already in use, change it in `.env` and restart:

```bash
# Edit .env and change to an available port
docker compose down && docker compose up -d
```

### Health check shows unhealthy

The container may need more time to start on first run or low-resource hosts. Check the logs:

```bash
docker compose logs
```

If needed, increase `start_period` in `docker-compose.yml`.

### Permission errors

Ensure the Docker user has write access to the data volume:

```bash
docker compose exec dokploy ls -la /data 2>/dev/null || echo "Volume directory not accessible"
```

## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

```bash
docker compose down
docker run --rm -v dokploy_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/dokploy-backup-$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
```

### Recovery

```bash
docker compose down
docker run --rm -v dokploy_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/dokploy-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
```

## Project Homepage

- **Project site:** [Dokploy](https://github.com/Dokploy/dokploy)
- **Docker Image:** `dokploy/dokploy:latest`
- **Issues:** [GitHub Issues](https://github.com/Dokploy/dokploy/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
