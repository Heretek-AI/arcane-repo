# Fossflow

Self-hosted Fossflow deployment via Docker

This template provides a containerized deployment of [Fossflow](https://github.com/stnsmith/fossflow) using Docker Compose.

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
| `fossflow` | docker.io/stnsmith/fossflow:latest | Main application service |
| `fossflow_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `FOSSFLOW_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs fossflow
```

**Port conflict:**
Edit `.env` and change `FOSSFLOW_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fossflow ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fossflow --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fossflow_data:/data -v $(pwd):/backup alpine tar czf /backup/fossflow-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fossflow_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fossflow-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Fossflow](https://github.com/stnsmith/fossflow)
- **Docker Image:** `docker.io/stnsmith/fossflow:latest`
- **Documentation:** [GitHub Wiki](https://github.com/stnsmith/fossflow/wiki)
- **Issues:** [GitHub Issues](https://github.com/stnsmith/fossflow/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
