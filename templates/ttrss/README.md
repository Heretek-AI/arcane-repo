# Ttrss

Self-hosted Ttrss deployment via Docker

This template provides a containerized deployment of [Ttrss](https://github.com/wangqiru/ttrss) using Docker Compose.

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
   curl -s http://localhost:80/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:80](http://localhost:80) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ttrss` | docker.io/wangqiru/ttrss:latest | Main application service |
| `ttrss_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `TTRSS_PORT` | `80` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs ttrss
```

**Port conflict:**
Edit `.env` and change `TTRSS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ttrss ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ttrss --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ttrss_data:/data -v $(pwd):/backup alpine tar czf /backup/ttrss-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ttrss_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ttrss-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Ttrss](https://github.com/wangqiru/ttrss)
- **Docker Image:** `docker.io/wangqiru/ttrss:latest`
- **Documentation:** [GitHub Wiki](https://github.com/wangqiru/ttrss/wiki)
- **Issues:** [GitHub Issues](https://github.com/wangqiru/ttrss/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
