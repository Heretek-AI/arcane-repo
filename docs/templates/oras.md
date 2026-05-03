---
title: "Oras"
description: "Self-hosted Oras deployment via Docker"
---

# Oras

Self-hosted Oras deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/priority" class="tag-badge">priority</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/oras/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/oras/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/oras/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `oras` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `889645e79319078e33f59f32a178cb4f154aeb26e0244862c164255bee6f3ac7` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `oras` | ghcr.io/oras-project/oras:latest | Main application service |
| `oras_data` | (volume) | Persistent data storage |

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
| `ORAS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs oras
```

**Port conflict:**
Edit `.env` and change `ORAS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec oras ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect oras --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v oras_data:/data -v $(pwd):/backup alpine tar czf /backup/oras-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v oras_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/oras-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Oras](https://github.com/oras-project/oras)
- **Docker Image:** `ghcr.io/oras-project/oras:latest`
- **Documentation:** [GitHub Wiki](https://github.com/oras-project/oras/wiki)
- **Issues:** [GitHub Issues](https://github.com/oras-project/oras/issues)

