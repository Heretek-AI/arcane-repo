---
title: "Baikal"
description: "Self-hosted Baikal deployment via Docker"
---

# Baikal

Self-hosted Baikal deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/baikal/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/baikal/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/baikal/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `baikal` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `262127290d3670b72ec514d57fef58c17bd937d33877c644523156d8e56000e5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `baikal` | docker.io/ckulka/baikal:latest | Main application service |
| `baikal_data` | (volume) | Persistent data storage |

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
| `BAIKAL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs baikal
```

**Port conflict:**
Edit `.env` and change `BAIKAL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec baikal ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect baikal --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v baikal_data:/data -v $(pwd):/backup alpine tar czf /backup/baikal-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v baikal_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/baikal-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Baikal](https://github.com/ckulka/baikal)
- **Docker Image:** `docker.io/ckulka/baikal:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ckulka/baikal/wiki)
- **Issues:** [GitHub Issues](https://github.com/ckulka/baikal/issues)

