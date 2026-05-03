---
title: "Seaweedfs"
description: "Self-hosted Seaweedfs deployment via Docker"
---

# Seaweedfs

Self-hosted Seaweedfs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/seaweedfs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/seaweedfs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/seaweedfs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `seaweedfs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e367da3902de4dd4ea2eb41cd391fc59fd799d98d3dab3b184cc25cc38f49e46` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `seaweedfs` | ghcr.io/seaweedfs/seaweedfs:latest | Main application service |
| `seaweedfs_data` | (volume) | Persistent data storage |

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
| `SEAWEEDFS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs seaweedfs
```

**Port conflict:**
Edit `.env` and change `SEAWEEDFS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec seaweedfs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect seaweedfs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v seaweedfs_data:/data -v $(pwd):/backup alpine tar czf /backup/seaweedfs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v seaweedfs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/seaweedfs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Seaweedfs](https://github.com/seaweedfs/seaweedfs)
- **Docker Image:** `ghcr.io/seaweedfs/seaweedfs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/seaweedfs/seaweedfs/wiki)
- **Issues:** [GitHub Issues](https://github.com/seaweedfs/seaweedfs/issues)

