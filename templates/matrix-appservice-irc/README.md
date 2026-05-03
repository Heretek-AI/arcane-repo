# Matrix Appservice Irc

Self-hosted Matrix Appservice Irc deployment via Docker

This template provides a containerized deployment of [Matrix Appservice Irc](https://github.com/matrixdotorg/matrix-appservice-irc) using Docker Compose.

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
   curl -s http://localhost:8008/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8008](http://localhost:8008) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `matrix-appservice-irc` | docker.io/matrixdotorg/matrix-appservice-irc:latest | Main application service |
| `matrix-appservice-irc_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MATRIX_APPSERVICE_IRC_PORT` | `8008` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs matrix-appservice-irc
```

**Port conflict:**
Edit `.env` and change `MATRIX-APPSERVICE-IRC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec matrix-appservice-irc ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect matrix-appservice-irc --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v matrix-appservice-irc_data:/data -v $(pwd):/backup alpine tar czf /backup/matrix-appservice-irc-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v matrix-appservice-irc_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/matrix-appservice-irc-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Matrix Appservice Irc](https://github.com/matrixdotorg/matrix-appservice-irc)
- **Docker Image:** `docker.io/matrixdotorg/matrix-appservice-irc:latest`
- **Documentation:** [GitHub Wiki](https://github.com/matrixdotorg/matrix-appservice-irc/wiki)
- **Issues:** [GitHub Issues](https://github.com/matrixdotorg/matrix-appservice-irc/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
