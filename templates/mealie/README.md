# Mealie

Self-hosted Mealie deployment via Docker

This template provides a containerized deployment of [Mealie](https://github.com/hkotel/mealie) using Docker Compose.

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
| `mealie` | docker.io/hkotel/mealie:latest | Main application service |
| `mealie_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MEALIE_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs mealie
```

**Port conflict:**
Edit `.env` and change `MEALIE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mealie ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mealie --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mealie_data:/data -v $(pwd):/backup alpine tar czf /backup/mealie-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mealie_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mealie-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Mealie](https://github.com/hkotel/mealie)
- **Docker Image:** `docker.io/hkotel/mealie:latest`
- **Documentation:** [GitHub Wiki](https://github.com/hkotel/mealie/wiki)
- **Issues:** [GitHub Issues](https://github.com/hkotel/mealie/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
