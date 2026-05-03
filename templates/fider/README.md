# Fider

Self-hosted Fider deployment via Docker

This template provides a containerized deployment of [Fider](https://github.com/getfider/fider) using Docker Compose.

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
| `fider` | docker.io/getfider/fider:latest | Main application service |
| `fider_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `FIDER_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs fider
```

**Port conflict:**
Edit `.env` and change `FIDER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fider ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fider --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fider_data:/data -v $(pwd):/backup alpine tar czf /backup/fider-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fider_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fider-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Fider](https://github.com/getfider/fider)
- **Docker Image:** `docker.io/getfider/fider:latest`
- **Documentation:** [GitHub Wiki](https://github.com/getfider/fider/wiki)
- **Issues:** [GitHub Issues](https://github.com/getfider/fider/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
