# Chatbot Ui

Self-hosted Chatbot Ui deployment via Docker

This template provides a containerized deployment of [Chatbot Ui](https://github.com/nmfretz/chatbot-ui) using Docker Compose.

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
   curl -s http://localhost:3000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `chatbot-ui` | ghcr.io/nmfretz/chatbot-ui:latest | Main application service |
| `chatbot-ui_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `CHATBOT_UI_PORT` | `3000` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs chatbot-ui
```

**Port conflict:**
Edit `.env` and change `CHATBOT-UI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec chatbot-ui ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect chatbot-ui --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v chatbot-ui_data:/data -v $(pwd):/backup alpine tar czf /backup/chatbot-ui-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v chatbot-ui_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/chatbot-ui-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Chatbot Ui](https://github.com/nmfretz/chatbot-ui)
- **Docker Image:** `ghcr.io/nmfretz/chatbot-ui:latest`
- **Documentation:** [GitHub Wiki](https://github.com/nmfretz/chatbot-ui/wiki)
- **Issues:** [GitHub Issues](https://github.com/nmfretz/chatbot-ui/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
