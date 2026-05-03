---
title: "Sonarr"
description: "Self-hosted Sonarr deployment via Docker"
---

# Sonarr

Self-hosted Sonarr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sonarr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sonarr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sonarr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sonarr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e7aa533b5d2e8ce18b194f383b173eb5dbcbb1430bfe0ebf8337c1e5fc335132` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `sonarr` | ghcr.io/linuxserver/sonarr:latest | Main application service |
| `sonarr_data` | (volume) | Persistent data storage |

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
| `SONARR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs sonarr
```

**Port conflict:**
Edit `.env` and change `SONARR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec sonarr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect sonarr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v sonarr_data:/data -v $(pwd):/backup alpine tar czf /backup/sonarr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v sonarr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/sonarr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Sonarr](https://github.com/linuxserver/sonarr)
- **Docker Image:** `ghcr.io/linuxserver/sonarr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/sonarr/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/sonarr/issues)

