---
title: "Tunarr"
description: "Self-hosted Tunarr deployment via Docker"
---

# Tunarr

Self-hosted Tunarr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tunarr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tunarr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tunarr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tunarr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6105492eedae571c9348d2879fb9df615b008d3938df3d8039f8cd5f1ba5930d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tunarr` | ghcr.io/chrisbenincasa/tunarr:latest | Main application service |
| `tunarr_data` | (volume) | Persistent data storage |

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
| `TUNARR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tunarr
```

**Port conflict:**
Edit `.env` and change `TUNARR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tunarr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tunarr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tunarr_data:/data -v $(pwd):/backup alpine tar czf /backup/tunarr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tunarr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tunarr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tunarr](https://github.com/chrisbenincasa/tunarr)
- **Docker Image:** `ghcr.io/chrisbenincasa/tunarr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/chrisbenincasa/tunarr/wiki)
- **Issues:** [GitHub Issues](https://github.com/chrisbenincasa/tunarr/issues)

