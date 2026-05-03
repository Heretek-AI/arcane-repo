---
title: "Jellyfin"
description: "Self-hosted Jellyfin deployment via Docker"
---

# Jellyfin

Self-hosted Jellyfin deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyfin/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyfin/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyfin/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `jellyfin` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d980fa6fc01862cc85a385cab3bdfc98b318d0cdd754634f0291df28142aa6b4` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `jellyfin` | ghcr.io/jellyfin/jellyfin:latest | Main application service |
| `jellyfin_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8096/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8096](http://localhost:8096) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `JELLYFIN_PORT` | `8096` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs jellyfin
```

**Port conflict:**
Edit `.env` and change `JELLYFIN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec jellyfin ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect jellyfin --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v jellyfin_data:/data -v $(pwd):/backup alpine tar czf /backup/jellyfin-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v jellyfin_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/jellyfin-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Jellyfin](https://github.com/jellyfin/jellyfin)
- **Docker Image:** `ghcr.io/jellyfin/jellyfin:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jellyfin/jellyfin/wiki)
- **Issues:** [GitHub Issues](https://github.com/jellyfin/jellyfin/issues)

