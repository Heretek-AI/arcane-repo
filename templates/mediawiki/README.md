# Mediawiki

Collaborative wiki platform

## Project Overview

[Mediawiki](https://github.com/wikimedia/mediawiki) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run Mediawiki in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `mediawiki` | `docker.io/library/mediawiki:latest` | Main application service |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `mediawiki_data` | (varies) | Persistent data storage |

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
curl -s http://localhost:80/ | head -c 200
```

### 4. Access the application

Open [http://localhost:80](http://localhost:80) in your browser.

## Configuration Reference

### Environment Variables

Set these in your `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MEDIAWIKI_PORT` | `80` | mediawiki host port (default: 80) |


## Troubleshooting

### Container won't start

Check the logs for error messages:

```bash
docker compose logs
```

### Port conflict

If the default port 80 is already in use, change it in `.env` and restart:

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
docker compose exec mediawiki ls -la /data 2>/dev/null || echo "Volume directory not accessible"
```

## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

```bash
docker compose down
docker run --rm -v mediawiki_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/mediawiki-backup-$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
```

### Recovery

```bash
docker compose down
docker run --rm -v mediawiki_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/mediawiki-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
```

## Project Homepage

- **Project site:** [Mediawiki](https://github.com/wikimedia/mediawiki)
- **Docker Image:** `docker.io/library/mediawiki:latest`
- **Issues:** [GitHub Issues](https://github.com/wikimedia/mediawiki/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
