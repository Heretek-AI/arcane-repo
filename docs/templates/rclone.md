---
title: "Rclone"
description: "Self-hosted Rclone deployment via Docker"
---

# Rclone

Self-hosted Rclone deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rclone/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rclone/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rclone/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `rclone` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c6e81dca40dbc912d86c539bc84818600bbf309f408c42ece914cab8b9c4dfbd` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `rclone` | ghcr.io/rclone/rclone:latest | Main application service |
| `rclone_data` | (volume) | Persistent data storage |

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
| `RCLONE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs rclone
```

**Port conflict:**
Edit `.env` and change `RCLONE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec rclone ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect rclone --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v rclone_data:/data -v $(pwd):/backup alpine tar czf /backup/rclone-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v rclone_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/rclone-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Rclone](https://github.com/rclone/rclone)
- **Docker Image:** `ghcr.io/rclone/rclone:latest`
- **Documentation:** [GitHub Wiki](https://github.com/rclone/rclone/wiki)
- **Issues:** [GitHub Issues](https://github.com/rclone/rclone/issues)

