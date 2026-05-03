---
title: "Fastapi"
description: "Self-hosted Fastapi deployment via Docker"
---

# Fastapi

Self-hosted Fastapi deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fastapi/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fastapi/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fastapi/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `fastapi` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `2dd4aeee6320167583c184c63a349c7e32295e9b10a89103d29b76053aa9c9e2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `fastapi` | docker.io/demisto/fastapi:latest | Main application service |
| `fastapi_data` | (volume) | Persistent data storage |

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
| `FASTAPI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs fastapi
```

**Port conflict:**
Edit `.env` and change `FASTAPI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fastapi ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fastapi --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fastapi_data:/data -v $(pwd):/backup alpine tar czf /backup/fastapi-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fastapi_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fastapi-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Fastapi](https://github.com/demisto/fastapi)
- **Docker Image:** `docker.io/demisto/fastapi:latest`
- **Documentation:** [GitHub Wiki](https://github.com/demisto/fastapi/wiki)
- **Issues:** [GitHub Issues](https://github.com/demisto/fastapi/issues)

