---
title: "Restic"
description: "Self-hosted Restic deployment via Docker"
---

# Restic

Self-hosted Restic deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/restic/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/restic/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/restic/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `restic` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8d05a89371c139eb2437b88b5dbc93c2c73a569ad873e735ffc16e6599dda1b9` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `restic` | ghcr.io/restic/restic:latest | Main application service |
| `restic_data` | (volume) | Persistent data storage |

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
| `RESTIC_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs restic
```

**Port conflict:**
Edit `.env` and change `RESTIC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec restic ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect restic --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v restic_data:/data -v $(pwd):/backup alpine tar czf /backup/restic-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v restic_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/restic-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Restic](https://github.com/restic/restic)
- **Docker Image:** `ghcr.io/restic/restic:latest`
- **Documentation:** [GitHub Wiki](https://github.com/restic/restic/wiki)
- **Issues:** [GitHub Issues](https://github.com/restic/restic/issues)

