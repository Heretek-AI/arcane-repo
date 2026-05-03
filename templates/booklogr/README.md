# Booklogr

Self-hosted Booklogr deployment via Docker, sourced from Awesome-Selfhosted catalog

This template provides a containerized deployment of [Booklogr](https://github.com/mozzo/booklogr) using Docker Compose.

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
| `booklogr` | docker.io/mozzo/booklogr:latest | Main application service |
| `booklogr_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `BOOKLOGR_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs booklogr
```

**Port conflict:**
Edit `.env` and change `BOOKLOGR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec booklogr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect booklogr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v booklogr_data:/data -v $(pwd):/backup alpine tar czf /backup/booklogr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v booklogr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/booklogr-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Booklogr](https://github.com/mozzo/booklogr)
- **Docker Image:** `docker.io/mozzo/booklogr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mozzo/booklogr/wiki)
- **Issues:** [GitHub Issues](https://github.com/mozzo/booklogr/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
