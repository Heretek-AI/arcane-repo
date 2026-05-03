# Plex

Self-hosted Plex deployment via Docker

This template provides a containerized deployment of [Plex](https://github.com/linuxserver/plex) using Docker Compose.

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
   curl -s http://localhost:32400/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:32400](http://localhost:32400) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `plex` | ghcr.io/linuxserver/plex:latest | Main application service |
| `plex_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PLEX_PORT` | `32400` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs plex
```

**Port conflict:**
Edit `.env` and change `PLEX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec plex ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect plex --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v plex_data:/data -v $(pwd):/backup alpine tar czf /backup/plex-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v plex_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/plex-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Plex](https://github.com/linuxserver/plex)
- **Docker Image:** `ghcr.io/linuxserver/plex:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/plex/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/plex/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
