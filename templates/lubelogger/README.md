# Lubelogger

Self-hosted Lubelogger deployment via Docker

This template provides a containerized deployment of [Lubelogger](https://github.com/hargata/lubelogger) using Docker Compose.

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
| `lubelogger` | ghcr.io/hargata/lubelogger:latest | Main application service |
| `lubelogger_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `LUBELOGGER_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs lubelogger
```

**Port conflict:**
Edit `.env` and change `LUBELOGGER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec lubelogger ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect lubelogger --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v lubelogger_data:/data -v $(pwd):/backup alpine tar czf /backup/lubelogger-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v lubelogger_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/lubelogger-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Lubelogger](https://github.com/hargata/lubelogger)
- **Docker Image:** `ghcr.io/hargata/lubelogger:latest`
- **Documentation:** [GitHub Wiki](https://github.com/hargata/lubelogger/wiki)
- **Issues:** [GitHub Issues](https://github.com/hargata/lubelogger/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
