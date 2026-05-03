---
title: "Matterbridge"
description: "Self-hosted Matterbridge deployment via Docker"
---

# Matterbridge

Self-hosted Matterbridge deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matterbridge/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matterbridge/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matterbridge/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `matterbridge` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b8ecf47208b7cae63a6abb2c4f301f2d1352df8fa6a81d957e3f9a1389529fe5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `matterbridge` | ghcr.io/42wim/matterbridge:latest | Main application service |
| `matterbridge_data` | (volume) | Persistent data storage |

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
| `MATTERBRIDGE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs matterbridge
```

**Port conflict:**
Edit `.env` and change `MATTERBRIDGE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec matterbridge ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect matterbridge --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v matterbridge_data:/data -v $(pwd):/backup alpine tar czf /backup/matterbridge-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v matterbridge_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/matterbridge-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Matterbridge](https://github.com/42wim/matterbridge)
- **Docker Image:** `ghcr.io/42wim/matterbridge:latest`
- **Documentation:** [GitHub Wiki](https://github.com/42wim/matterbridge/wiki)
- **Issues:** [GitHub Issues](https://github.com/42wim/matterbridge/issues)

