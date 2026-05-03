# What To Cook?

Self-hosted What To Cook? deployment via Docker

This template provides a containerized deployment of [What To Cook?](https://github.com/kassner/whattocook) using Docker Compose.

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
| `what-to-cook` | ghcr.io/kassner/whattocook:latest | Main application service |
| `what-to-cook_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WHAT_TO_COOK_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs what-to-cook
```

**Port conflict:**
Edit `.env` and change `WHAT-TO-COOK_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec what-to-cook ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect what-to-cook --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v what-to-cook_data:/data -v $(pwd):/backup alpine tar czf /backup/what-to-cook-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v what-to-cook_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/what-to-cook-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [What To Cook?](https://github.com/kassner/whattocook)
- **Docker Image:** `ghcr.io/kassner/whattocook:latest`
- **Documentation:** [GitHub Wiki](https://github.com/kassner/whattocook/wiki)
- **Issues:** [GitHub Issues](https://github.com/kassner/whattocook/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
