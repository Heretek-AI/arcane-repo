# Pixel Server

Self-hosted Pixel Server deployment via Docker

This template provides a containerized deployment of [Pixel Server](https://github.com/olegvorobyov90/pixel-server) using Docker Compose.

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
| `pixel-server` | docker.io/olegvorobyov90/pixel-server:latest | Main application service |
| `pixel-server_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PIXEL_SERVER_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs pixel-server
```

**Port conflict:**
Edit `.env` and change `PIXEL-SERVER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pixel-server ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pixel-server --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pixel-server_data:/data -v $(pwd):/backup alpine tar czf /backup/pixel-server-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pixel-server_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pixel-server-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Pixel Server](https://github.com/olegvorobyov90/pixel-server)
- **Docker Image:** `docker.io/olegvorobyov90/pixel-server:latest`
- **Documentation:** [GitHub Wiki](https://github.com/olegvorobyov90/pixel-server/wiki)
- **Issues:** [GitHub Issues](https://github.com/olegvorobyov90/pixel-server/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
