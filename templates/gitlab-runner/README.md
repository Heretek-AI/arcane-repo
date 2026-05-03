# Gitlab Runner

Self-hosted Gitlab Runner deployment via Docker

This template provides a containerized deployment of [Gitlab Runner](https://github.com/gitlab/gitlab-runner) using Docker Compose.

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
| `gitlab-runner` | docker.io/gitlab/gitlab-runner:latest | Main application service |
| `gitlab-runner_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `GITLAB_RUNNER_PORT` | `80` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs gitlab-runner
```

**Port conflict:**
Edit `.env` and change `GITLAB-RUNNER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gitlab-runner ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gitlab-runner --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gitlab-runner_data:/data -v $(pwd):/backup alpine tar czf /backup/gitlab-runner-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gitlab-runner_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gitlab-runner-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Gitlab Runner](https://github.com/gitlab/gitlab-runner)
- **Docker Image:** `docker.io/gitlab/gitlab-runner:latest`
- **Documentation:** [GitHub Wiki](https://github.com/gitlab/gitlab-runner/wiki)
- **Issues:** [GitHub Issues](https://github.com/gitlab/gitlab-runner/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
