# Test Application

A test template for verifying the build-registry script

This template provides a containerized deployment of [Test Application](test application) using Docker Compose.

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
| `app` | nginx:latest | Main application service |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `80` | Configuration variable |
| `HOST` | `0.0.0.0` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs app
```

**Port conflict:**
Edit `.env` and change `TEST-APP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec app ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect test-app --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v test-app_data:/data -v $(pwd):/backup alpine tar czf /backup/test-app-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v test-app_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/test-app-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Docker Image:** `nginx:latest`


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
