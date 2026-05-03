# Warpgate

Self-hosted Warpgate deployment via Docker

This template provides a containerized deployment of [Warpgate](https://github.com/heywoodlh/warpgate) using Docker Compose.

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
| `warpgate` | docker.io/heywoodlh/warpgate:latest | Main application service |
| `warpgate_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WARPGATE_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs warpgate
```

**Port conflict:**
Edit `.env` and change `WARPGATE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec warpgate ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect warpgate --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v warpgate_data:/data -v $(pwd):/backup alpine tar czf /backup/warpgate-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v warpgate_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/warpgate-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Warpgate](https://github.com/heywoodlh/warpgate)
- **Docker Image:** `docker.io/heywoodlh/warpgate:latest`
- **Documentation:** [GitHub Wiki](https://github.com/heywoodlh/warpgate/wiki)
- **Issues:** [GitHub Issues](https://github.com/heywoodlh/warpgate/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
