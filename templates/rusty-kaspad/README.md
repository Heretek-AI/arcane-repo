# Rusty Kaspad

Self-hosted Rusty Kaspad deployment via Docker

This template provides a containerized deployment of [Rusty Kaspad](https://github.com/kaspanet/rusty-kaspad) using Docker Compose.

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
| `rusty-kaspad` | docker.io/kaspanet/rusty-kaspad:latest | Main application service |
| `rusty-kaspad_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `RUSTY_KASPAD_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs rusty-kaspad
```

**Port conflict:**
Edit `.env` and change `RUSTY-KASPAD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec rusty-kaspad ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect rusty-kaspad --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v rusty-kaspad_data:/data -v $(pwd):/backup alpine tar czf /backup/rusty-kaspad-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v rusty-kaspad_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/rusty-kaspad-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Rusty Kaspad](https://github.com/kaspanet/rusty-kaspad)
- **Docker Image:** `docker.io/kaspanet/rusty-kaspad:latest`
- **Documentation:** [GitHub Wiki](https://github.com/kaspanet/rusty-kaspad/wiki)
- **Issues:** [GitHub Issues](https://github.com/kaspanet/rusty-kaspad/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
