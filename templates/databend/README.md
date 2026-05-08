# Databend

Cloud-native data warehouse

## Project Overview

[Databend](https://github.com/databendlabs/databend) is a self-hosted deployment packaged as a Docker Compose template. This template provides everything needed to run Databend in a containerized environment with persistent storage, health checks, and environment-based configuration.

## Architecture

### Services

| Service | Image | Purpose |
|---------|-------|---------|
| `databend` | `datafuselabs/databend:latest` | Main application service |

### Volumes

| Volume | Mount | Purpose |
|--------|-------|---------|
| `databend_data` | (varies) | Persistent data storage |

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
curl -s http://localhost:8000/ | head -c 200
```

### 4. Access the application

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration Reference

### Environment Variables

Set these in your `.env` file (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABEND_PORT` | `8000` | mysql -h 127.0.0.1 -P 8000 -u root |
| `DATABEND_HTTP_PORT` | `8124` | HTTP handler port for REST API queries (default: 8124) |
| `QUERY_DEFAULT_USER` | `root` | Query user credentials (default: root with no password) |
| `QUERY_DEFAULT_PASSWORD` | `—` | QUERY_DEFAULT_PASSWORD configuration value |
| `QUERY_STORAGE_TYPE` | `fs` | Storage backend: 'fs' (local filesystem) or 's3' |
| `AWS_S3_ENDPOINT` | `https://s3.amazonaws.com` | Set QUERY_STORAGE_TYPE=s3 and configure: |
| `AWS_S3_BUCKET` | `my-databend-bucket` | AWS_S3_BUCKET configuration value |
| `AWS_ACCESS_KEY_ID` | `your-access-key` | AWS_ACCESS_KEY_ID configuration value |
| `AWS_SECRET_ACCESS_KEY` | `your-secret-key` | AWS_SECRET_ACCESS_KEY configuration value |
| `MINIO_ENABLED` | `false` | container for local object storage testing. MinIO available on port 9000. |
| `DATABEND_MINIO_PORT` | `9000` | Host port for embedded MinIO S3-compatible API (default: 9000) |


## Troubleshooting

### Container won't start

Check the logs for error messages:

```bash
docker compose logs
```

### Port conflict

If the default port 8000 is already in use, change it in `.env` and restart:

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
docker compose exec databend ls -la /data 2>/dev/null || echo "Volume directory not accessible"
```

## Backup & Recovery

### Backup

Stop the service to ensure data consistency, then back up the data volume:

```bash
docker compose down
docker run --rm -v databend_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/databend-backup-$(date +%Y%m%d).tar.gz -C /data .
docker compose up -d
```

### Recovery

```bash
docker compose down
docker run --rm -v databend_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/databend-backup-YYYYMMDD.tar.gz -C /data
docker compose up -d
```

## Project Homepage

- **Project site:** [Databend](https://github.com/databendlabs/databend)
- **Docker Image:** `datafuselabs/databend:latest`
- **Issues:** [GitHub Issues](https://github.com/databendlabs/databend/issues)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
