# Marreta

Self-hosted Marreta deployment via Docker

This template provides a containerized deployment of [Marreta](https://github.com/manualdousuario/marreta) using Docker Compose.

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
| `marreta` | ghcr.io/manualdousuario/marreta:latest | Main application service |
| `marreta_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MARRETA_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs marreta
```

**Port conflict:**
Edit `.env` and change `MARRETA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec marreta ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect marreta --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v marreta_data:/data -v $(pwd):/backup alpine tar czf /backup/marreta-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v marreta_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/marreta-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Marreta](https://github.com/manualdousuario/marreta)
- **Docker Image:** `ghcr.io/manualdousuario/marreta:latest`
- **Documentation:** [GitHub Wiki](https://github.com/manualdousuario/marreta/wiki)
- **Issues:** [GitHub Issues](https://github.com/manualdousuario/marreta/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
