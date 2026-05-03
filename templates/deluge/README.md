# Deluge

Self-hosted Deluge deployment via Docker

This template provides a containerized deployment of [Deluge](https://github.com/linuxserver/deluge) using Docker Compose.

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
   curl -s http://localhost:8112/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8112](http://localhost:8112) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `deluge` | ghcr.io/linuxserver/deluge:latest | Main application service |
| `deluge_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DELUGE_PORT` | `8112` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs deluge
```

**Port conflict:**
Edit `.env` and change `DELUGE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec deluge ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect deluge --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v deluge_data:/data -v $(pwd):/backup alpine tar czf /backup/deluge-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v deluge_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/deluge-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Deluge](https://github.com/linuxserver/deluge)
- **Docker Image:** `ghcr.io/linuxserver/deluge:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/deluge/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/deluge/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
