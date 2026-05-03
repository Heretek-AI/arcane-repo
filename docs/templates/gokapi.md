---
title: "Gokapi"
description: "Self-hosted Gokapi deployment via Docker"
---

# Gokapi

Self-hosted Gokapi deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gokapi/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gokapi/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gokapi/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gokapi` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b1edae930fbffb9894a2adfc22205d471df5bdb29883a0497e7a8e5be1c1261b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gokapi` | docker.io/f0rc3/gokapi:latest | Main application service |
| `gokapi_data` | (volume) | Persistent data storage |

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
| `GOKAPI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gokapi
```

**Port conflict:**
Edit `.env` and change `GOKAPI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gokapi ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gokapi --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gokapi_data:/data -v $(pwd):/backup alpine tar czf /backup/gokapi-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gokapi_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gokapi-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gokapi](https://github.com/f0rc3/gokapi)
- **Docker Image:** `docker.io/f0rc3/gokapi:latest`
- **Documentation:** [GitHub Wiki](https://github.com/f0rc3/gokapi/wiki)
- **Issues:** [GitHub Issues](https://github.com/f0rc3/gokapi/issues)

