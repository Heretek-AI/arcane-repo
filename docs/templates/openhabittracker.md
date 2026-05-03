---
title: "Openhabittracker"
description: "Self-hosted Openhabittracker deployment via Docker"
---

# Openhabittracker

Self-hosted Openhabittracker deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openhabittracker/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openhabittracker/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openhabittracker/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openhabittracker` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a117eae33f6061a7288cb51fb3a06b6f81d22ac3298ff2022c21d6bc0d00fd4f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `openhabittracker` | docker.io/jinjinov/openhabittracker:latest | Main application service |
| `openhabittracker_data` | (volume) | Persistent data storage |

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
| `OPENHABITTRACKER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs openhabittracker
```

**Port conflict:**
Edit `.env` and change `OPENHABITTRACKER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec openhabittracker ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect openhabittracker --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v openhabittracker_data:/data -v $(pwd):/backup alpine tar czf /backup/openhabittracker-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v openhabittracker_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/openhabittracker-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Openhabittracker](https://github.com/jinjinov/openhabittracker)
- **Docker Image:** `docker.io/jinjinov/openhabittracker:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jinjinov/openhabittracker/wiki)
- **Issues:** [GitHub Issues](https://github.com/jinjinov/openhabittracker/issues)

