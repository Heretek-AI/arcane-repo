# Matomo

Privacy-friendly web analytics

## Project Overview

[Matomo](https://github.com/matomo-org/matomo) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run Matomo in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `matomo` | `docker.io/library/matomo:latest` | Main application service |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `matomo_data` | (varies) | Persistent data storage |

### Health Check

The container runs a health check every 30s (3 retries, 30s start period). Docker will report the container as unhealthy if the endpoint fails consistently.

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
curl -s http://localhost:8080/ | head -c 200
```

### 4. Access the application

Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration Reference

### Environment Variables

Set these in your `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MATOMO_PORT` | `8080` | Matomo host port (default: 8080) |


## Troubleshooting

### Container won't start

Check the logs for error messages:

```bash
docker compose logs
```

### Port conflict

If the default port 8080 is already in use, change it in `.env` and restart:

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
docker compose exec matomo ls -la /data 2>/dev/null || echo "Volume directory not accessible"
```

## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

```bash
docker compose down
docker run --rm -v matomo_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/matomo-backup-$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
```

### Recovery

```bash
docker compose down
docker run --rm -v matomo_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/matomo-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
```

## Project Homepage

- **Project site:** [Matomo](https://github.com/matomo-org/matomo)
- **Docker Image:** `docker.io/library/matomo:latest`
- **Issues:** [GitHub Issues](https://github.com/matomo-org/matomo/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
