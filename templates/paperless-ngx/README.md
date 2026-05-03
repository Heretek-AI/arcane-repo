# Paperless Ngx

Self-hosted document management system that scans, indexes, and archives paper documents with full-text search

This template provides a containerized deployment of [Paperless Ngx](https://github.com/paperless-ngx/paperless-ngx) using Docker Compose.

## Quick Start

1. **Clone and configure:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Verify it's running:**

   ```bash
   docker compose ps
   curl -s http://localhost:8000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `paperless-ngx` | ghcr.io/paperless-ngx/paperless-ngx:latest | Main application service |
| `paperless-ngx_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PAPERLESS_NGX_PORT` | `8000` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs paperless-ngx
```

**Port conflict:**
Edit `.env` and change `PAPERLESS-NGX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec paperless-ngx ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect paperless-ngx --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v paperless-ngx_data:/data -v $(pwd):/backup alpine tar czf /backup/paperless-ngx-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v paperless-ngx_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/paperless-ngx-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Paperless Ngx](https://github.com/paperless-ngx/paperless-ngx)
- **Docker Image:** `ghcr.io/paperless-ngx/paperless-ngx:latest`
- **Documentation:** [GitHub Wiki](https://github.com/paperless-ngx/paperless-ngx/wiki)
- **Issues:** [GitHub Issues](https://github.com/paperless-ngx/paperless-ngx/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
