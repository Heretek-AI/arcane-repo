---
title: "Apprise Api"
description: "Self-hosted Apprise Api deployment via Docker"
---

# Apprise Api

Self-hosted Apprise Api deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/apprise-api/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/apprise-api/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/apprise-api/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `apprise-api` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `36dc6beaa2413f7def0e2d132fb8a2db393f3aa1fef069533e965ce4ff9d0821` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `apprise-api` | ghcr.io/linuxserver/apprise-api:latest | Main application service |
| `apprise-api_data` | (volume) | Persistent data storage |

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
| `APPRISE_API_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs apprise-api
```

**Port conflict:**
Edit `.env` and change `APPRISE-API_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec apprise-api ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect apprise-api --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v apprise-api_data:/data -v $(pwd):/backup alpine tar czf /backup/apprise-api-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v apprise-api_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/apprise-api-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Apprise Api](https://github.com/linuxserver/apprise-api)
- **Docker Image:** `ghcr.io/linuxserver/apprise-api:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/apprise-api/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/apprise-api/issues)

