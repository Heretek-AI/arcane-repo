# Terraforming Mars

Self-hosted Terraforming Mars deployment via Docker

This template provides a containerized deployment of [Terraforming Mars](https://github.com/andrewsav/terraforming-mars) using Docker Compose.

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
| `terraforming-mars` | docker.io/andrewsav/terraforming-mars:latest | Main application service |
| `terraforming-mars_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `TERRAFORMING_MARS_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs terraforming-mars
```

**Port conflict:**
Edit `.env` and change `TERRAFORMING-MARS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec terraforming-mars ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect terraforming-mars --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v terraforming-mars_data:/data -v $(pwd):/backup alpine tar czf /backup/terraforming-mars-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v terraforming-mars_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/terraforming-mars-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Terraforming Mars](https://github.com/andrewsav/terraforming-mars)
- **Docker Image:** `docker.io/andrewsav/terraforming-mars:latest`
- **Documentation:** [GitHub Wiki](https://github.com/andrewsav/terraforming-mars/wiki)
- **Issues:** [GitHub Issues](https://github.com/andrewsav/terraforming-mars/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
