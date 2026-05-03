---
title: "Silverbullet"
description: "Self-hosted Silverbullet deployment via Docker"
---

# Silverbullet

Self-hosted Silverbullet deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/silverbullet/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/silverbullet/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/silverbullet/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `silverbullet` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d21594e7f609d5815f884973f12846a71ed439d249c7afee95c9b4c9df4af8ac` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `silverbullet` | docker.io/zefhemel/silverbullet:latest | Main application service |
| `silverbullet_data` | (volume) | Persistent data storage |

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
| `SILVERBULLET_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs silverbullet
```

**Port conflict:**
Edit `.env` and change `SILVERBULLET_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec silverbullet ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect silverbullet --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v silverbullet_data:/data -v $(pwd):/backup alpine tar czf /backup/silverbullet-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v silverbullet_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/silverbullet-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Silverbullet](https://github.com/zefhemel/silverbullet)
- **Docker Image:** `docker.io/zefhemel/silverbullet:latest`
- **Documentation:** [GitHub Wiki](https://github.com/zefhemel/silverbullet/wiki)
- **Issues:** [GitHub Issues](https://github.com/zefhemel/silverbullet/issues)

