---
title: "Backrest"
description: "Self-hosted Backrest deployment via Docker"
---

# Backrest

Self-hosted Backrest deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/backrest/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/backrest/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/backrest/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `backrest` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `eb0ca843c2d88f56ac3d3a14e73bca12ff609223ca92d0998e2b5ba7133d05aa` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `backrest` | ghcr.io/garethgeorge/backrest:latest | Main application service |
| `backrest_data` | (volume) | Persistent data storage |

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
| `BACKREST_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs backrest
```

**Port conflict:**
Edit `.env` and change `BACKREST_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec backrest ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect backrest --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v backrest_data:/data -v $(pwd):/backup alpine tar czf /backup/backrest-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v backrest_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/backrest-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Backrest](https://github.com/garethgeorge/backrest)
- **Docker Image:** `ghcr.io/garethgeorge/backrest:latest`
- **Documentation:** [GitHub Wiki](https://github.com/garethgeorge/backrest/wiki)
- **Issues:** [GitHub Issues](https://github.com/garethgeorge/backrest/issues)

