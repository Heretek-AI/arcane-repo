# Facilmap

Self-hosted Facilmap deployment via Docker

This template provides a containerized deployment of [Facilmap](https://github.com/facilmap/facilmap) using Docker Compose.

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
| `facilmap` | docker.io/facilmap/facilmap:latest | Main application service |
| `facilmap_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `FACILMAP_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs facilmap
```

**Port conflict:**
Edit `.env` and change `FACILMAP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec facilmap ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect facilmap --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v facilmap_data:/data -v $(pwd):/backup alpine tar czf /backup/facilmap-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v facilmap_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/facilmap-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Facilmap](https://github.com/facilmap/facilmap)
- **Docker Image:** `docker.io/facilmap/facilmap:latest`
- **Documentation:** [GitHub Wiki](https://github.com/facilmap/facilmap/wiki)
- **Issues:** [GitHub Issues](https://github.com/facilmap/facilmap/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
