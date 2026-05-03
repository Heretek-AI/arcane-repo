---
title: "Mqttx Web"
description: "Self-hosted Mqttx Web deployment via Docker"
---

# Mqttx Web

Self-hosted Mqttx Web deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mqttx-web/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mqttx-web/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mqttx-web/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mqttx-web` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f9e6b41ea92f1025bbfc573d26b7c41506db98e08b7d58048ed388964bb252d7` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mqttx-web` | docker.io/emqx/mqttx-web:latest | Main application service |
| `mqttx-web_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

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

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MQTTX_WEB_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mqttx-web
```

**Port conflict:**
Edit `.env` and change `MQTTX-WEB_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mqttx-web ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mqttx-web --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mqttx-web_data:/data -v $(pwd):/backup alpine tar czf /backup/mqttx-web-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mqttx-web_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mqttx-web-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mqttx Web](https://github.com/emqx/mqttx-web)
- **Docker Image:** `docker.io/emqx/mqttx-web:latest`
- **Documentation:** [GitHub Wiki](https://github.com/emqx/mqttx-web/wiki)
- **Issues:** [GitHub Issues](https://github.com/emqx/mqttx-web/issues)

