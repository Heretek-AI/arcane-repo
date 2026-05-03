# Woodpecker

Self-hosted Woodpecker deployment via Docker

This template provides a containerized deployment of [Woodpecker](https://github.com/daemonless/woodpecker) using Docker Compose.

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
   curl -s http://localhost:8000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `woodpecker` | ghcr.io/daemonless/woodpecker:latest | Main application service |
| `woodpecker_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WOODPECKER_PORT` | `8000` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs woodpecker
```

**Port conflict:**
Edit `.env` and change `WOODPECKER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec woodpecker ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect woodpecker --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v woodpecker_data:/data -v $(pwd):/backup alpine tar czf /backup/woodpecker-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v woodpecker_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/woodpecker-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Woodpecker](https://github.com/daemonless/woodpecker)
- **Docker Image:** `ghcr.io/daemonless/woodpecker:latest`
- **Documentation:** [GitHub Wiki](https://github.com/daemonless/woodpecker/wiki)
- **Issues:** [GitHub Issues](https://github.com/daemonless/woodpecker/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
