---
title: "Morphos"
description: "Self-hosted Morphos deployment via Docker"
---

# Morphos

Self-hosted Morphos deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/morphos/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/morphos/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/morphos/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `morphos` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c194da9eae45b310ec33a0bb26335a81d3fc95205040b2094c28f3d48e256cbe` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `morphos` | docker.io/wapmorgan/morphos:latest | Main application service |
| `morphos_data` | (volume) | Persistent data storage |

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
| `MORPHOS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs morphos
```

**Port conflict:**
Edit `.env` and change `MORPHOS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec morphos ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect morphos --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v morphos_data:/data -v $(pwd):/backup alpine tar czf /backup/morphos-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v morphos_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/morphos-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Morphos](https://github.com/wapmorgan/morphos)
- **Docker Image:** `docker.io/wapmorgan/morphos:latest`
- **Documentation:** [GitHub Wiki](https://github.com/wapmorgan/morphos/wiki)
- **Issues:** [GitHub Issues](https://github.com/wapmorgan/morphos/issues)

