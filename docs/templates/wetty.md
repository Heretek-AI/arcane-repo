---
title: "Wetty"
description: "Self-hosted Wetty deployment via Docker"
---

# Wetty

Self-hosted Wetty deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wetty/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wetty/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wetty/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `wetty` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `644ce35781be04385b19af5ff9b34d6b4ff93b3bac0e37ebd8db76fa2d565d3d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `wetty` | ghcr.io/butlerx/wetty:latest | Main application service |
| `wetty_data` | (volume) | Persistent data storage |

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
| `WETTY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs wetty
```

**Port conflict:**
Edit `.env` and change `WETTY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec wetty ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect wetty --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v wetty_data:/data -v $(pwd):/backup alpine tar czf /backup/wetty-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v wetty_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/wetty-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Wetty](https://github.com/butlerx/wetty)
- **Docker Image:** `ghcr.io/butlerx/wetty:latest`
- **Documentation:** [GitHub Wiki](https://github.com/butlerx/wetty/wiki)
- **Issues:** [GitHub Issues](https://github.com/butlerx/wetty/issues)

