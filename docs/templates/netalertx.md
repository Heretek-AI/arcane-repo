---
title: "Netalertx"
description: "Self-hosted Netalertx deployment via Docker"
---

# Netalertx

Self-hosted Netalertx deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netalertx/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netalertx/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netalertx/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `netalertx` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d06edb4d82de1cea7d5fa6f9d86996ea2617b6d699c481ebfa58f5bffd4c814a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `netalertx` | ghcr.io/netalertx/netalertx:latest | Main application service |
| `netalertx_data` | (volume) | Persistent data storage |

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
| `NETALERTX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs netalertx
```

**Port conflict:**
Edit `.env` and change `NETALERTX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec netalertx ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect netalertx --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v netalertx_data:/data -v $(pwd):/backup alpine tar czf /backup/netalertx-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v netalertx_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/netalertx-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Netalertx](https://github.com/netalertx/netalertx)
- **Docker Image:** `ghcr.io/netalertx/netalertx:latest`
- **Documentation:** [GitHub Wiki](https://github.com/netalertx/netalertx/wiki)
- **Issues:** [GitHub Issues](https://github.com/netalertx/netalertx/issues)

