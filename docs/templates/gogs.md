---
title: "Gogs"
description: "Self-hosted Gogs deployment via Docker"
---

# Gogs

Self-hosted Gogs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gogs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gogs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gogs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gogs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `30ea58df56f7f02bdea167001df26bb3fe5274f6009a85f9de45f5f0affee5a3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gogs` | ghcr.io/gogs/gogs:latest | Main application service |
| `gogs_data` | (volume) | Persistent data storage |

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
| `GOGS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gogs
```

**Port conflict:**
Edit `.env` and change `GOGS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gogs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gogs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gogs_data:/data -v $(pwd):/backup alpine tar czf /backup/gogs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gogs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gogs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gogs](https://github.com/gogs/gogs)
- **Docker Image:** `ghcr.io/gogs/gogs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/gogs/gogs/wiki)
- **Issues:** [GitHub Issues](https://github.com/gogs/gogs/issues)

