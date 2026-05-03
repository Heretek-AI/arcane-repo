---
title: "Facilmap"
description: "Self-hosted Facilmap deployment via Docker"
---

# Facilmap

Self-hosted Facilmap deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/facilmap/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/facilmap/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/facilmap/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `facilmap` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `71db2025f254f7e72656c4175e462f8b8ed228bbc96a296107b5e1760fc63445` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `facilmap` | docker.io/facilmap/facilmap:latest | Main application service |
| `facilmap_data` | (volume) | Persistent data storage |

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
| `FACILMAP_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs facilmap
```

**Port conflict:**
Edit `.env` and change `FACILMAP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec facilmap ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect facilmap --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v facilmap_data:/data -v $(pwd):/backup alpine tar czf /backup/facilmap-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v facilmap_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/facilmap-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Facilmap](https://github.com/facilmap/facilmap)
- **Docker Image:** `docker.io/facilmap/facilmap:latest`
- **Documentation:** [GitHub Wiki](https://github.com/facilmap/facilmap/wiki)
- **Issues:** [GitHub Issues](https://github.com/facilmap/facilmap/issues)

