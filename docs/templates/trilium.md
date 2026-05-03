---
title: "Trilium"
description: "Self-hosted Trilium deployment via Docker"
---

# Trilium

Self-hosted Trilium deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trilium/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trilium/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trilium/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `trilium` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d5cdfe5ddf1e411d118fa51606af0568aacf3ebf4d7cbfde2715650a9de8211f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `trilium` | ghcr.io/zadam/trilium:latest | Main application service |
| `trilium_data` | (volume) | Persistent data storage |

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
| `TRILIUM_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs trilium
```

**Port conflict:**
Edit `.env` and change `TRILIUM_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec trilium ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect trilium --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v trilium_data:/data -v $(pwd):/backup alpine tar czf /backup/trilium-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v trilium_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/trilium-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Trilium](https://github.com/zadam/trilium)
- **Docker Image:** `ghcr.io/zadam/trilium:latest`
- **Documentation:** [GitHub Wiki](https://github.com/zadam/trilium/wiki)
- **Issues:** [GitHub Issues](https://github.com/zadam/trilium/issues)

