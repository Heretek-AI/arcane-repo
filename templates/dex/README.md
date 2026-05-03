# Dex

Self-hosted Dex deployment via Docker

This template provides a containerized deployment of [Dex](https://github.com/dexidp/dex) using Docker Compose.

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
| `dex` | ghcr.io/dexidp/dex:latest | Main application service |
| `dex_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DEX_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs dex
```

**Port conflict:**
Edit `.env` and change `DEX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dex ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dex --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dex_data:/data -v $(pwd):/backup alpine tar czf /backup/dex-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dex_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dex-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Dex](https://github.com/dexidp/dex)
- **Docker Image:** `ghcr.io/dexidp/dex:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dexidp/dex/wiki)
- **Issues:** [GitHub Issues](https://github.com/dexidp/dex/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
