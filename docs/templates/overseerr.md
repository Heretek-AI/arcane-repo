---
title: "Overseerr"
description: "Self-hosted Overseerr deployment via Docker"
---

# Overseerr

Self-hosted Overseerr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/overseerr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/overseerr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/overseerr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `overseerr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d46423c266223e10a7c56c0ad4eaf10c3d8ca0109f84dcd66946987967501ba2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `overseerr` | docker.io/sctx/overseerr:latest | Main application service |
| `overseerr_data` | (volume) | Persistent data storage |

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
| `OVERSEERR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs overseerr
```

**Port conflict:**
Edit `.env` and change `OVERSEERR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec overseerr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect overseerr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v overseerr_data:/data -v $(pwd):/backup alpine tar czf /backup/overseerr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v overseerr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/overseerr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Overseerr](https://github.com/sctx/overseerr)
- **Docker Image:** `docker.io/sctx/overseerr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sctx/overseerr/wiki)
- **Issues:** [GitHub Issues](https://github.com/sctx/overseerr/issues)

