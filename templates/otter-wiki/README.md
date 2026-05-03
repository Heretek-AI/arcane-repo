# Otter Wiki

Self-hosted Otter Wiki deployment via Docker

This template provides a containerized deployment of [Otter Wiki](https://github.com/redimp/otterwiki) using Docker Compose.

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
| `otter-wiki` | docker.io/redimp/otterwiki:latest | Main application service |
| `otter-wiki_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OTTER_WIKI_PORT` | `80` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs otter-wiki
```

**Port conflict:**
Edit `.env` and change `OTTER-WIKI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec otter-wiki ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect otter-wiki --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v otter-wiki_data:/data -v $(pwd):/backup alpine tar czf /backup/otter-wiki-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v otter-wiki_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/otter-wiki-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Otter Wiki](https://github.com/redimp/otterwiki)
- **Docker Image:** `docker.io/redimp/otterwiki:latest`
- **Documentation:** [GitHub Wiki](https://github.com/redimp/otterwiki/wiki)
- **Issues:** [GitHub Issues](https://github.com/redimp/otterwiki/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
