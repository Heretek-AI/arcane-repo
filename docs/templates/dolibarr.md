---
title: "Dolibarr"
description: "Self-hosted Dolibarr deployment via Docker"
---

# Dolibarr

Self-hosted Dolibarr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dolibarr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dolibarr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dolibarr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dolibarr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4dd6b6aaba2088d679ac043aa1e34f0c014d23b9b6a01ed1d7191f35697fe9f5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dolibarr` | docker.io/dolibarr/dolibarr:latest | Main application service |
| `dolibarr_data` | (volume) | Persistent data storage |

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
| `DOLIBARR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dolibarr
```

**Port conflict:**
Edit `.env` and change `DOLIBARR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dolibarr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dolibarr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dolibarr_data:/data -v $(pwd):/backup alpine tar czf /backup/dolibarr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dolibarr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dolibarr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dolibarr](https://github.com/dolibarr/dolibarr)
- **Docker Image:** `docker.io/dolibarr/dolibarr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dolibarr/dolibarr/wiki)
- **Issues:** [GitHub Issues](https://github.com/dolibarr/dolibarr/issues)

