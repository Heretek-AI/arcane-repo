# Pyload Ng

Self-hosted Pyload Ng deployment via Docker

This template provides a containerized deployment of [Pyload Ng](https://github.com/linuxserver/pyload-ng) using Docker Compose.

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
| `pyload-ng` | ghcr.io/linuxserver/pyload-ng:latest | Main application service |
| `pyload-ng_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PYLOAD_NG_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs pyload-ng
```

**Port conflict:**
Edit `.env` and change `PYLOAD-NG_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pyload-ng ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pyload-ng --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pyload-ng_data:/data -v $(pwd):/backup alpine tar czf /backup/pyload-ng-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pyload-ng_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pyload-ng-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Pyload Ng](https://github.com/linuxserver/pyload-ng)
- **Docker Image:** `ghcr.io/linuxserver/pyload-ng:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/pyload-ng/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/pyload-ng/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
