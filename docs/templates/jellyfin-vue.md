---
title: "Jellyfin Vue"
description: "Self-hosted Jellyfin Vue deployment via Docker"
---

# Jellyfin Vue

Self-hosted Jellyfin Vue deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyfin-vue/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyfin-vue/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyfin-vue/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `jellyfin-vue` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6130730452559e52bd59acccb068a9b1029cb6d8776068b7e17c5ac03bd9a3a1` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `jellyfin-vue` | ghcr.io/jellyfin/jellyfin-vue:latest | Main application service |
| `jellyfin-vue_data` | (volume) | Persistent data storage |

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
| `JELLYFIN_VUE_PORT` | `8096` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs jellyfin-vue
```

**Port conflict:**
Edit `.env` and change `JELLYFIN-VUE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec jellyfin-vue ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect jellyfin-vue --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v jellyfin-vue_data:/data -v $(pwd):/backup alpine tar czf /backup/jellyfin-vue-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v jellyfin-vue_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/jellyfin-vue-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Jellyfin Vue](https://github.com/jellyfin/jellyfin-vue)
- **Docker Image:** `ghcr.io/jellyfin/jellyfin-vue:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jellyfin/jellyfin-vue/wiki)
- **Issues:** [GitHub Issues](https://github.com/jellyfin/jellyfin-vue/issues)

