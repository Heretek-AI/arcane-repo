---
title: "Ittools"
description: "Self-hosted Ittools deployment via Docker"
---

# Ittools

Self-hosted Ittools deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ittools/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ittools/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ittools/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ittools` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3d0f7f92209d1f78f60f0d97992bdb0e25b07307781991db6afbe12dd254d899` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ittools` | docker.io/bordercolli/ittools:latest | Main application service |
| `ittools_data` | (volume) | Persistent data storage |

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
| `ITTOOLS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs ittools
```

**Port conflict:**
Edit `.env` and change `ITTOOLS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ittools ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ittools --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ittools_data:/data -v $(pwd):/backup alpine tar czf /backup/ittools-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ittools_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ittools-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Ittools](https://github.com/bordercolli/ittools)
- **Docker Image:** `docker.io/bordercolli/ittools:latest`
- **Documentation:** [GitHub Wiki](https://github.com/bordercolli/ittools/wiki)
- **Issues:** [GitHub Issues](https://github.com/bordercolli/ittools/issues)

