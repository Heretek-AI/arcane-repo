# Transmission

Self-hosted Transmission deployment via Docker

This template provides a containerized deployment of [Transmission](https://github.com/linuxserver/transmission) using Docker Compose.

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
   curl -s http://localhost:9091/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9091](http://localhost:9091) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `transmission` | ghcr.io/linuxserver/transmission:latest | Main application service |
| `transmission_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `TRANSMISSION_PORT` | `9091` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs transmission
```

**Port conflict:**
Edit `.env` and change `TRANSMISSION_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec transmission ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect transmission --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v transmission_data:/data -v $(pwd):/backup alpine tar czf /backup/transmission-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v transmission_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/transmission-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Transmission](https://github.com/linuxserver/transmission)
- **Docker Image:** `ghcr.io/linuxserver/transmission:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/transmission/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/transmission/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
