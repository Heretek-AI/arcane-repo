---
title: "Tinyfilemanager"
description: "Self-hosted Tinyfilemanager deployment via Docker"
---

# Tinyfilemanager

Self-hosted Tinyfilemanager deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/storage" class="tag-badge">storage</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tinyfilemanager/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tinyfilemanager/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tinyfilemanager/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tinyfilemanager` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1badd00e3f711d309d0e98609ddf8d21a0e85d28285e907b9223f58cb7aaeb88` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tinyfilemanager` | docker.io/tinyfilemanager/tinyfilemanager:latest | Main application service |
| `tinyfilemanager_data` | (volume) | Persistent data storage |

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
| `TINYFILEMANAGER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tinyfilemanager
```

**Port conflict:**
Edit `.env` and change `TINYFILEMANAGER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tinyfilemanager ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tinyfilemanager --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tinyfilemanager_data:/data -v $(pwd):/backup alpine tar czf /backup/tinyfilemanager-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tinyfilemanager_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tinyfilemanager-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tinyfilemanager](https://github.com/tinyfilemanager/tinyfilemanager)
- **Docker Image:** `docker.io/tinyfilemanager/tinyfilemanager:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tinyfilemanager/tinyfilemanager/wiki)
- **Issues:** [GitHub Issues](https://github.com/tinyfilemanager/tinyfilemanager/issues)

