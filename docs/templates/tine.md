---
title: "Tine"
description: "Self-hosted Tine deployment via Docker"
---

# Tine

Self-hosted Tine deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tine/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tine/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tine/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tine` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1392be0d2ec980a43becd5dd8faf5aca978b57fa6275a6111fba77a82faf1e8a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tine` | docker.io/tinegroupware/tine:latest | Main application service |
| `tine_data` | (volume) | Persistent data storage |

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
| `TINE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tine
```

**Port conflict:**
Edit `.env` and change `TINE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tine ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tine --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tine_data:/data -v $(pwd):/backup alpine tar czf /backup/tine-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tine_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tine-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tine](https://github.com/tinegroupware/tine)
- **Docker Image:** `docker.io/tinegroupware/tine:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tinegroupware/tine/wiki)
- **Issues:** [GitHub Issues](https://github.com/tinegroupware/tine/issues)

