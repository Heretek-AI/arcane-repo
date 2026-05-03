# Slash

Self-hosted Slash deployment via Docker

This template provides a containerized deployment of [Slash](https://github.com/yourselfhosted/slash) using Docker Compose.

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
| `slash` | docker.io/yourselfhosted/slash:latest | Main application service |
| `slash_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SLASH_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs slash
```

**Port conflict:**
Edit `.env` and change `SLASH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec slash ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect slash --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v slash_data:/data -v $(pwd):/backup alpine tar czf /backup/slash-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v slash_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/slash-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Slash](https://github.com/yourselfhosted/slash)
- **Docker Image:** `docker.io/yourselfhosted/slash:latest`
- **Documentation:** [GitHub Wiki](https://github.com/yourselfhosted/slash/wiki)
- **Issues:** [GitHub Issues](https://github.com/yourselfhosted/slash/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
