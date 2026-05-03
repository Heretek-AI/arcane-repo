# Directorylister

Self-hosted Directorylister deployment via Docker

This template provides a containerized deployment of [Directorylister](https://github.com/directorylister/directorylister) using Docker Compose.

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
| `directorylister` | docker.io/directorylister/directorylister:latest | Main application service |
| `directorylister_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DIRECTORYLISTER_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs directorylister
```

**Port conflict:**
Edit `.env` and change `DIRECTORYLISTER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec directorylister ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect directorylister --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v directorylister_data:/data -v $(pwd):/backup alpine tar czf /backup/directorylister-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v directorylister_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/directorylister-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Directorylister](https://github.com/directorylister/directorylister)
- **Docker Image:** `docker.io/directorylister/directorylister:latest`
- **Documentation:** [GitHub Wiki](https://github.com/directorylister/directorylister/wiki)
- **Issues:** [GitHub Issues](https://github.com/directorylister/directorylister/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
