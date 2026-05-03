---
title: "Flame"
description: "Self-hosted Flame deployment via Docker"
---

# Flame

Self-hosted Flame deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flame/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flame/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flame/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flame` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ec3451f352f0ee997c81bd5b00aca014856e221aa4a212fff7663ab0c8ff23a3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `flame` | docker.io/pawelmalak/flame:latest | Main application service |
| `flame_data` | (volume) | Persistent data storage |

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
| `FLAME_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs flame
```

**Port conflict:**
Edit `.env` and change `FLAME_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec flame ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect flame --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v flame_data:/data -v $(pwd):/backup alpine tar czf /backup/flame-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v flame_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/flame-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Flame](https://github.com/pawelmalak/flame)
- **Docker Image:** `docker.io/pawelmalak/flame:latest`
- **Documentation:** [GitHub Wiki](https://github.com/pawelmalak/flame/wiki)
- **Issues:** [GitHub Issues](https://github.com/pawelmalak/flame/issues)

