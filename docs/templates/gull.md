---
title: "Gull"
description: "Self-hosted Gull deployment via Docker"
---

# Gull

Self-hosted Gull deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gull/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gull/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gull/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gull` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a10372f79503c537a85a54dad21030a0a5351bea27e51423ae1947f7d4e79988` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gull` | ghcr.io/aeolyus/gull:latest | Main application service |
| `gull_data` | (volume) | Persistent data storage |

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
| `GULL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gull
```

**Port conflict:**
Edit `.env` and change `GULL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gull ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gull --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gull_data:/data -v $(pwd):/backup alpine tar czf /backup/gull-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gull_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gull-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gull](https://github.com/aeolyus/gull)
- **Docker Image:** `ghcr.io/aeolyus/gull:latest`
- **Documentation:** [GitHub Wiki](https://github.com/aeolyus/gull/wiki)
- **Issues:** [GitHub Issues](https://github.com/aeolyus/gull/issues)

