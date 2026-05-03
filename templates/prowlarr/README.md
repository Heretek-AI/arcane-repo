# Prowlarr

Self-hosted Prowlarr deployment via Docker

This template provides a containerized deployment of [Prowlarr](https://github.com/linuxserver/prowlarr) using Docker Compose.

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
| `prowlarr` | ghcr.io/linuxserver/prowlarr:latest | Main application service |
| `prowlarr_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PROWLARR_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs prowlarr
```

**Port conflict:**
Edit `.env` and change `PROWLARR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec prowlarr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect prowlarr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v prowlarr_data:/data -v $(pwd):/backup alpine tar czf /backup/prowlarr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v prowlarr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/prowlarr-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Prowlarr](https://github.com/linuxserver/prowlarr)
- **Docker Image:** `ghcr.io/linuxserver/prowlarr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/prowlarr/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/prowlarr/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
