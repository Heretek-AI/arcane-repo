# Filegator

Self-hosted Filegator deployment via Docker

This template provides a containerized deployment of [Filegator](https://github.com/filegator/filegator) using Docker Compose.

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
| `filegator` | docker.io/filegator/filegator:latest | Main application service |
| `filegator_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `FILEGATOR_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs filegator
```

**Port conflict:**
Edit `.env` and change `FILEGATOR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec filegator ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect filegator --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v filegator_data:/data -v $(pwd):/backup alpine tar czf /backup/filegator-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v filegator_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/filegator-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Filegator](https://github.com/filegator/filegator)
- **Docker Image:** `docker.io/filegator/filegator:latest`
- **Documentation:** [GitHub Wiki](https://github.com/filegator/filegator/wiki)
- **Issues:** [GitHub Issues](https://github.com/filegator/filegator/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
