---
title: "Qflood"
description: "Self-hosted Qflood deployment via Docker"
---

# Qflood

Self-hosted Qflood deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/qflood/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/qflood/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/qflood/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `qflood` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7319dff6712e737d851ef5d1f11f4af970a13484356425659ce4c68be8c25a00` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `qflood` | ghcr.io/engels74/qflood:latest | Main application service |
| `qflood_data` | (volume) | Persistent data storage |

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
| `QFLOOD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs qflood
```

**Port conflict:**
Edit `.env` and change `QFLOOD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec qflood ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect qflood --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v qflood_data:/data -v $(pwd):/backup alpine tar czf /backup/qflood-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v qflood_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/qflood-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Qflood](https://github.com/engels74/qflood)
- **Docker Image:** `ghcr.io/engels74/qflood:latest`
- **Documentation:** [GitHub Wiki](https://github.com/engels74/qflood/wiki)
- **Issues:** [GitHub Issues](https://github.com/engels74/qflood/issues)

