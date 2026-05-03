# Elasticsearch8

Self-hosted Elasticsearch8 deployment via Docker

This template provides a containerized deployment of [Elasticsearch8](https://github.com/danielberteaud/elasticsearch8) using Docker Compose.

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
   curl -s http://localhost:9200/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9200](http://localhost:9200) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `elasticsearch8` | docker.io/danielberteaud/elasticsearch8:latest | Main application service |
| `elasticsearch8_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `ELASTICSEARCH8_PORT` | `9200` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs elasticsearch8
```

**Port conflict:**
Edit `.env` and change `ELASTICSEARCH8_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec elasticsearch8 ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect elasticsearch8 --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v elasticsearch8_data:/data -v $(pwd):/backup alpine tar czf /backup/elasticsearch8-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v elasticsearch8_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/elasticsearch8-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Elasticsearch8](https://github.com/danielberteaud/elasticsearch8)
- **Docker Image:** `docker.io/danielberteaud/elasticsearch8:latest`
- **Documentation:** [GitHub Wiki](https://github.com/danielberteaud/elasticsearch8/wiki)
- **Issues:** [GitHub Issues](https://github.com/danielberteaud/elasticsearch8/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
