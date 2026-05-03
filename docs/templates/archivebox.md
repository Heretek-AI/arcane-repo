---
title: "Archivebox"
description: "Self-hosted Archivebox deployment via Docker"
---

# Archivebox

Self-hosted Archivebox deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/archivebox/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/archivebox/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/archivebox/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `archivebox` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8d3505a085c894a2fd1565ae595300f8d80760ebd7956506516d9426f92fb674` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `archivebox` | ghcr.io/archivebox/archivebox:latest | Main application service |
| `archivebox_data` | (volume) | Persistent data storage |

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
| `ARCHIVEBOX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs archivebox
```

**Port conflict:**
Edit `.env` and change `ARCHIVEBOX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec archivebox ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect archivebox --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v archivebox_data:/data -v $(pwd):/backup alpine tar czf /backup/archivebox-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v archivebox_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/archivebox-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Archivebox](https://github.com/archivebox/archivebox)
- **Docker Image:** `ghcr.io/archivebox/archivebox:latest`
- **Documentation:** [GitHub Wiki](https://github.com/archivebox/archivebox/wiki)
- **Issues:** [GitHub Issues](https://github.com/archivebox/archivebox/issues)

