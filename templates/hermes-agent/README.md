# Hermes Agent

Self-hosted Hermes Agent deployment via Docker

This template provides a containerized deployment of [Hermes Agent](https://github.com/nousresearch/hermes-agent) using Docker Compose.

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
| `hermes-agent` | docker.io/nousresearch/hermes-agent:latest | Main application service |
| `hermes-agent_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `HERMES_AGENT_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs hermes-agent
```

**Port conflict:**
Edit `.env` and change `HERMES-AGENT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec hermes-agent ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect hermes-agent --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v hermes-agent_data:/data -v $(pwd):/backup alpine tar czf /backup/hermes-agent-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v hermes-agent_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/hermes-agent-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Hermes Agent](https://github.com/nousresearch/hermes-agent)
- **Docker Image:** `docker.io/nousresearch/hermes-agent:latest`
- **Documentation:** [GitHub Wiki](https://github.com/nousresearch/hermes-agent/wiki)
- **Issues:** [GitHub Issues](https://github.com/nousresearch/hermes-agent/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
