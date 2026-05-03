---
title: "Fab Manager"
description: "Self-hosted Fab Manager deployment via Docker"
---

# Fab Manager

Self-hosted Fab Manager deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fab-manager/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fab-manager/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fab-manager/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `fab-manager` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7dbb2ad55687e737948e53dad1c71ecd7ff0a26bfb06edd52c763bf943c0515b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `fab-manager` | docker.io/sleede/fab-manager:latest | Main application service |
| `fab-manager_data` | (volume) | Persistent data storage |

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
| `FAB_MANAGER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs fab-manager
```

**Port conflict:**
Edit `.env` and change `FAB-MANAGER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fab-manager ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fab-manager --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fab-manager_data:/data -v $(pwd):/backup alpine tar czf /backup/fab-manager-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fab-manager_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fab-manager-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Fab Manager](https://github.com/sleede/fab-manager)
- **Docker Image:** `docker.io/sleede/fab-manager:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sleede/fab-manager/wiki)
- **Issues:** [GitHub Issues](https://github.com/sleede/fab-manager/issues)

