---
title: "Calibre Web Automated"
description: "Self-hosted Calibre Web Automated deployment via Docker"
---

# Calibre Web Automated

Self-hosted Calibre Web Automated deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/calibre-web-automated/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/calibre-web-automated/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/calibre-web-automated/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `calibre-web-automated` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `17d12f3624b7b7f3129854a1ddb0e89d35b72b507e986a9ca8a2be206b282c6e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `calibre-web-automated` | ghcr.io/crocodilestick/calibre-web-automated:latest | Main application service |
| `calibre-web-automated_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8083/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8083](http://localhost:8083) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `CALIBRE_WEB_AUTOMATED_PORT` | `8083` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs calibre-web-automated
```

**Port conflict:**
Edit `.env` and change `CALIBRE-WEB-AUTOMATED_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec calibre-web-automated ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect calibre-web-automated --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v calibre-web-automated_data:/data -v $(pwd):/backup alpine tar czf /backup/calibre-web-automated-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v calibre-web-automated_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/calibre-web-automated-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Calibre Web Automated](https://github.com/crocodilestick/calibre-web-automated)
- **Docker Image:** `ghcr.io/crocodilestick/calibre-web-automated:latest`
- **Documentation:** [GitHub Wiki](https://github.com/crocodilestick/calibre-web-automated/wiki)
- **Issues:** [GitHub Issues](https://github.com/crocodilestick/calibre-web-automated/issues)

