# Uptime Kuma

Self-hosted monitoring tool for tracking uptime of websites, APIs, databases, and services with alerting

This template provides a containerized deployment of [Uptime Kuma](https://github.com/louislam/uptime-kuma) using Docker Compose.

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
   curl -s http://localhost:3001/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:3001](http://localhost:3001) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `uptime-kuma` | ghcr.io/louislam/uptime-kuma:latest | Main application service |
| `uptime-kuma_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `UPTIME_KUMA_PORT` | `3001` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs uptime-kuma
```

**Port conflict:**
Edit `.env` and change `UPTIME-KUMA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec uptime-kuma ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect uptime-kuma --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v uptime-kuma_data:/data -v $(pwd):/backup alpine tar czf /backup/uptime-kuma-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v uptime-kuma_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/uptime-kuma-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Uptime Kuma](https://github.com/louislam/uptime-kuma)
- **Docker Image:** `ghcr.io/louislam/uptime-kuma:latest`
- **Documentation:** [GitHub Wiki](https://github.com/louislam/uptime-kuma/wiki)
- **Issues:** [GitHub Issues](https://github.com/louislam/uptime-kuma/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
