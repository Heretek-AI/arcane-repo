---
title: "Jellyseerr"
description: "Self-hosted Jellyseerr deployment via Docker"
---

# Jellyseerr

Self-hosted Jellyseerr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyseerr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyseerr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jellyseerr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `jellyseerr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `266208b8cf6e2e3cb59a8a22913d7ee0988ef19cdc3f16852f6ff407c0165052` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `jellyseerr` | ghcr.io/fallenbagel/jellyseerr:latest | Main application service |
| `jellyseerr_data` | (volume) | Persistent data storage |

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
| `JELLYSEERR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs jellyseerr
```

**Port conflict:**
Edit `.env` and change `JELLYSEERR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec jellyseerr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect jellyseerr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v jellyseerr_data:/data -v $(pwd):/backup alpine tar czf /backup/jellyseerr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v jellyseerr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/jellyseerr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Jellyseerr](https://github.com/fallenbagel/jellyseerr)
- **Docker Image:** `ghcr.io/fallenbagel/jellyseerr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/fallenbagel/jellyseerr/wiki)
- **Issues:** [GitHub Issues](https://github.com/fallenbagel/jellyseerr/issues)

