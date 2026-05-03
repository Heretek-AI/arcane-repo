---
title: "Yarr"
description: "Self-hosted Yarr deployment via Docker"
---

# Yarr

Self-hosted Yarr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yarr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yarr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yarr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `yarr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `10f25385f0312cdb79f5986654b10c6c3c3c6117400f2799ebdf38c5c8e7f9fb` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `yarr` | ghcr.io/arsfeld/yarr:latest | Main application service |
| `yarr_data` | (volume) | Persistent data storage |

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
| `YARR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs yarr
```

**Port conflict:**
Edit `.env` and change `YARR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec yarr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect yarr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v yarr_data:/data -v $(pwd):/backup alpine tar czf /backup/yarr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v yarr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/yarr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Yarr](https://github.com/arsfeld/yarr)
- **Docker Image:** `ghcr.io/arsfeld/yarr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/arsfeld/yarr/wiki)
- **Issues:** [GitHub Issues](https://github.com/arsfeld/yarr/issues)

