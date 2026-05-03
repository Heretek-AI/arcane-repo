---
title: "Kanboard"
description: "Self-hosted Kanboard deployment via Docker"
---

# Kanboard

Self-hosted Kanboard deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kanboard/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kanboard/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kanboard/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `kanboard` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9d56b4978a1ca2c07dd288ee073ac6c1494eca802c270e0f025b76c00e85c519` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `kanboard` | ghcr.io/kanboard/kanboard:latest | Main application service |
| `kanboard_data` | (volume) | Persistent data storage |

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
| `KANBOARD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs kanboard
```

**Port conflict:**
Edit `.env` and change `KANBOARD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec kanboard ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect kanboard --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v kanboard_data:/data -v $(pwd):/backup alpine tar czf /backup/kanboard-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v kanboard_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/kanboard-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Kanboard](https://github.com/kanboard/kanboard)
- **Docker Image:** `ghcr.io/kanboard/kanboard:latest`
- **Documentation:** [GitHub Wiki](https://github.com/kanboard/kanboard/wiki)
- **Issues:** [GitHub Issues](https://github.com/kanboard/kanboard/issues)

