# Kavita

Self-hosted Kavita deployment via Docker

This template provides a containerized deployment of [Kavita](https://github.com/jvmilazz0/kavita) using Docker Compose.

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
| `kavita` | docker.io/jvmilazz0/kavita:latest | Main application service |
| `kavita_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `KAVITA_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs kavita
```

**Port conflict:**
Edit `.env` and change `KAVITA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec kavita ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect kavita --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v kavita_data:/data -v $(pwd):/backup alpine tar czf /backup/kavita-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v kavita_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/kavita-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Kavita](https://github.com/jvmilazz0/kavita)
- **Docker Image:** `docker.io/jvmilazz0/kavita:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jvmilazz0/kavita/wiki)
- **Issues:** [GitHub Issues](https://github.com/jvmilazz0/kavita/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
