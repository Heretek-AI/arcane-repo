# Photoshow

Self-hosted Photoshow deployment via Docker

This template provides a containerized deployment of [Photoshow](https://github.com/linuxserver/photoshow) using Docker Compose.

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
| `photoshow` | ghcr.io/linuxserver/photoshow:latest | Main application service |
| `photoshow_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PHOTOSHOW_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs photoshow
```

**Port conflict:**
Edit `.env` and change `PHOTOSHOW_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec photoshow ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect photoshow --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v photoshow_data:/data -v $(pwd):/backup alpine tar czf /backup/photoshow-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v photoshow_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/photoshow-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Photoshow](https://github.com/linuxserver/photoshow)
- **Docker Image:** `ghcr.io/linuxserver/photoshow:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/photoshow/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/photoshow/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
