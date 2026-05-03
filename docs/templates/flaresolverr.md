---
title: "Flaresolverr"
description: "Self-hosted Flaresolverr deployment via Docker"
---

# Flaresolverr

Self-hosted Flaresolverr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flaresolverr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flaresolverr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flaresolverr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flaresolverr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f84809f063a35b0e98d392445be2684a53f79841fb8a4e4323e50117730da828` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `flaresolverr` | ghcr.io/flaresolverr/flaresolverr:latest | Main application service |
| `flaresolverr_data` | (volume) | Persistent data storage |

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
| `FLARESOLVERR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs flaresolverr
```

**Port conflict:**
Edit `.env` and change `FLARESOLVERR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec flaresolverr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect flaresolverr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v flaresolverr_data:/data -v $(pwd):/backup alpine tar czf /backup/flaresolverr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v flaresolverr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/flaresolverr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Flaresolverr](https://github.com/flaresolverr/flaresolverr)
- **Docker Image:** `ghcr.io/flaresolverr/flaresolverr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/flaresolverr/flaresolverr/wiki)
- **Issues:** [GitHub Issues](https://github.com/flaresolverr/flaresolverr/issues)

