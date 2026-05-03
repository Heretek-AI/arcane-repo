# Starbase 80

Self-hosted Starbase 80 deployment via Docker

This template provides a containerized deployment of [Starbase 80](https://github.com/notclickable-jordan/starbase-80) using Docker Compose.

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
| `starbase-80` | ghcr.io/notclickable-jordan/starbase-80:latest | Main application service |
| `starbase-80_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `STARBASE_80_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs starbase-80
```

**Port conflict:**
Edit `.env` and change `STARBASE-80_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec starbase-80 ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect starbase-80 --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v starbase-80_data:/data -v $(pwd):/backup alpine tar czf /backup/starbase-80-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v starbase-80_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/starbase-80-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Starbase 80](https://github.com/notclickable-jordan/starbase-80)
- **Docker Image:** `ghcr.io/notclickable-jordan/starbase-80:latest`
- **Documentation:** [GitHub Wiki](https://github.com/notclickable-jordan/starbase-80/wiki)
- **Issues:** [GitHub Issues](https://github.com/notclickable-jordan/starbase-80/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
