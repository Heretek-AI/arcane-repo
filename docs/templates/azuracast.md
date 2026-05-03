---
title: "Azuracast"
description: "Self-hosted web radio management suite with live broadcasting, media library management, and listener analytics."
---

# Azuracast

Self-hosted web radio management suite with live broadcasting, media library management, and listener analytics.

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/azuracast/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/azuracast/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/azuracast/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `azuracast` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `950c31820e4de5bc2c640e8554d3364fcd52f95531e4217a6a805bd822aea579` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `azuracast` | ghcr.io/azuracast/azuracast:latest | Main application service |
| `azuracast_data` | (volume) | Persistent data storage |

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
| `AZURACAST_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs azuracast
```

**Port conflict:**
Edit `.env` and change `AZURACAST_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec azuracast ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect azuracast --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v azuracast_data:/data -v $(pwd):/backup alpine tar czf /backup/azuracast-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v azuracast_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/azuracast-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Azuracast](https://github.com/azuracast/azuracast)
- **Docker Image:** `ghcr.io/azuracast/azuracast:latest`
- **Documentation:** [GitHub Wiki](https://github.com/azuracast/azuracast/wiki)
- **Issues:** [GitHub Issues](https://github.com/azuracast/azuracast/issues)

