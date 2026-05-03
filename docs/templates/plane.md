---
title: "Plane"
description: "Self-hosted Plane deployment via Docker"
---

# Plane

Self-hosted Plane deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plane/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plane/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/plane/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `plane` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f74ca846de60d7c90f790b0dd8aa28b7de77f2a0281133bb750593a777ea874f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `plane` | docker.io/plane/plane:latest | Main application service |
| `plane_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PLANE_PORT` | `8000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs plane
```

**Port conflict:**
Edit `.env` and change `PLANE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec plane ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect plane --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v plane_data:/data -v $(pwd):/backup alpine tar czf /backup/plane-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v plane_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/plane-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Plane](https://github.com/plane/plane)
- **Docker Image:** `docker.io/plane/plane:latest`
- **Documentation:** [GitHub Wiki](https://github.com/plane/plane/wiki)
- **Issues:** [GitHub Issues](https://github.com/plane/plane/issues)

