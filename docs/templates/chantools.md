---
title: "Chantools"
description: "Self-hosted Chantools deployment via Docker"
---

# Chantools

Self-hosted Chantools deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chantools/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chantools/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chantools/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `chantools` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e074ac890e2cbb270459ff8ecf68a8c1f256aca6b801d32b5d8f290b760ade57` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `chantools` | docker.io/guggero/chantools:latest | Main application service |
| `chantools_data` | (volume) | Persistent data storage |

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
| `CHANTOOLS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs chantools
```

**Port conflict:**
Edit `.env` and change `CHANTOOLS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec chantools ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect chantools --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v chantools_data:/data -v $(pwd):/backup alpine tar czf /backup/chantools-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v chantools_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/chantools-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Chantools](https://github.com/guggero/chantools)
- **Docker Image:** `docker.io/guggero/chantools:latest`
- **Documentation:** [GitHub Wiki](https://github.com/guggero/chantools/wiki)
- **Issues:** [GitHub Issues](https://github.com/guggero/chantools/issues)

