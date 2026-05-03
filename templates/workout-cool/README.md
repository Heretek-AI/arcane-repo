# Workout Cool

Self-hosted Workout Cool deployment via Docker

This template provides a containerized deployment of [Workout Cool](https://github.com/xiaogblw/workout-cool) using Docker Compose.

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
| `workout-cool` | docker.io/xiaogblw/workout-cool:latest | Main application service |
| `workout-cool_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKOUT_COOL_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs workout-cool
```

**Port conflict:**
Edit `.env` and change `WORKOUT-COOL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec workout-cool ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect workout-cool --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v workout-cool_data:/data -v $(pwd):/backup alpine tar czf /backup/workout-cool-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v workout-cool_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/workout-cool-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Workout Cool](https://github.com/xiaogblw/workout-cool)
- **Docker Image:** `docker.io/xiaogblw/workout-cool:latest`
- **Documentation:** [GitHub Wiki](https://github.com/xiaogblw/workout-cool/wiki)
- **Issues:** [GitHub Issues](https://github.com/xiaogblw/workout-cool/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
