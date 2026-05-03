# Gonic

Self-hosted Gonic deployment via Docker

This template provides a containerized deployment of [Gonic](https://github.com/sentriz/gonic) using Docker Compose.

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
| `gonic` | ghcr.io/sentriz/gonic:latest | Main application service |
| `gonic_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `GONIC_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs gonic
```

**Port conflict:**
Edit `.env` and change `GONIC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gonic ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gonic --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gonic_data:/data -v $(pwd):/backup alpine tar czf /backup/gonic-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gonic_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gonic-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Gonic](https://github.com/sentriz/gonic)
- **Docker Image:** `ghcr.io/sentriz/gonic:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sentriz/gonic/wiki)
- **Issues:** [GitHub Issues](https://github.com/sentriz/gonic/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
