---
title: "Lidarr"
description: "Self-hosted Lidarr deployment via Docker"
---

# Lidarr

Self-hosted Lidarr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lidarr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lidarr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lidarr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `lidarr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3ec67059c6071382ed2d1d61e01bb9801ca61e3277e3aaf40d474a8d803ba089` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `lidarr` | ghcr.io/linuxserver/lidarr:latest | Main application service |
| `lidarr_data` | (volume) | Persistent data storage |

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
| `LIDARR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs lidarr
```

**Port conflict:**
Edit `.env` and change `LIDARR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec lidarr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect lidarr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v lidarr_data:/data -v $(pwd):/backup alpine tar czf /backup/lidarr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v lidarr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/lidarr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Lidarr](https://github.com/linuxserver/lidarr)
- **Docker Image:** `ghcr.io/linuxserver/lidarr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/lidarr/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/lidarr/issues)

