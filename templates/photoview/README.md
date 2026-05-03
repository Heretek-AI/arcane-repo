# Photoview

Self-hosted Photoview deployment via Docker

This template provides a containerized deployment of [Photoview](https://github.com/photoview/photoview) using Docker Compose.

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
   curl -s http://localhost:8080/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `photoview` | docker.io/photoview/photoview:latest | Main application service |
| `photoview_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PHOTOVIEW_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs photoview
```

**Port conflict:**
Edit `.env` and change `PHOTOVIEW_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec photoview ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect photoview --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v photoview_data:/data -v $(pwd):/backup alpine tar czf /backup/photoview-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v photoview_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/photoview-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Photoview](https://github.com/photoview/photoview)
- **Docker Image:** `docker.io/photoview/photoview:latest`
- **Documentation:** [GitHub Wiki](https://github.com/photoview/photoview/wiki)
- **Issues:** [GitHub Issues](https://github.com/photoview/photoview/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
