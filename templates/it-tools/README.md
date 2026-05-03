# It Tools

Self-hosted It Tools deployment via Docker

This template provides a containerized deployment of [It Tools](https://github.com/corentinth/it-tools) using Docker Compose.

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
| `it-tools` | ghcr.io/corentinth/it-tools:latest | Main application service |
| `it-tools_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `IT_TOOLS_PORT` | `80` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs it-tools
```

**Port conflict:**
Edit `.env` and change `IT-TOOLS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec it-tools ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect it-tools --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v it-tools_data:/data -v $(pwd):/backup alpine tar czf /backup/it-tools-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v it-tools_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/it-tools-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [It Tools](https://github.com/corentinth/it-tools)
- **Docker Image:** `ghcr.io/corentinth/it-tools:latest`
- **Documentation:** [GitHub Wiki](https://github.com/corentinth/it-tools/wiki)
- **Issues:** [GitHub Issues](https://github.com/corentinth/it-tools/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
