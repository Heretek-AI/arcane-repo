---
title: "Ubooquity"
description: "Self-hosted Ubooquity deployment via Docker"
---

# Ubooquity

Self-hosted Ubooquity deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ubooquity/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ubooquity/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ubooquity/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ubooquity` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8c058770b0ff3001a97f9597f6a748e7f51c55fb758949cb7ac86f0fb6b30c8e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ubooquity` | ghcr.io/linuxserver/ubooquity:latest | Main application service |
| `ubooquity_data` | (volume) | Persistent data storage |

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
| `UBOOQUITY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs ubooquity
```

**Port conflict:**
Edit `.env` and change `UBOOQUITY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ubooquity ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ubooquity --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ubooquity_data:/data -v $(pwd):/backup alpine tar czf /backup/ubooquity-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ubooquity_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ubooquity-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Ubooquity](https://github.com/linuxserver/ubooquity)
- **Docker Image:** `ghcr.io/linuxserver/ubooquity:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/ubooquity/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/ubooquity/issues)

