---
title: "Paaster"
description: "Self-hosted Paaster deployment via Docker"
---

# Paaster

Self-hosted Paaster deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/paaster/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/paaster/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/paaster/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `paaster` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1e9ea42c84d35b6cd1ca5d148781d233000071cd1eb68f1a6162c3271b0ceb94` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `paaster` | docker.io/wardpearce/paaster:latest | Main application service |
| `paaster_data` | (volume) | Persistent data storage |

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
| `PAASTER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs paaster
```

**Port conflict:**
Edit `.env` and change `PAASTER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec paaster ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect paaster --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v paaster_data:/data -v $(pwd):/backup alpine tar czf /backup/paaster-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v paaster_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/paaster-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Paaster](https://github.com/wardpearce/paaster)
- **Docker Image:** `docker.io/wardpearce/paaster:latest`
- **Documentation:** [GitHub Wiki](https://github.com/wardpearce/paaster/wiki)
- **Issues:** [GitHub Issues](https://github.com/wardpearce/paaster/issues)

