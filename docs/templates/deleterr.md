---
title: "Deleterr"
description: "Self-hosted Deleterr deployment via Docker"
---

# Deleterr

Self-hosted Deleterr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deleterr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deleterr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/deleterr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `deleterr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3cbdd1c4965c5c70dd905e9e88229a1dcd010706296337fe9a84d0fd8c25cfa5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `deleterr` | ghcr.io/rfsbraz/deleterr:latest | Main application service |
| `deleterr_data` | (volume) | Persistent data storage |

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
| `DELETERR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs deleterr
```

**Port conflict:**
Edit `.env` and change `DELETERR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec deleterr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect deleterr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v deleterr_data:/data -v $(pwd):/backup alpine tar czf /backup/deleterr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v deleterr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/deleterr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Deleterr](https://github.com/rfsbraz/deleterr)
- **Docker Image:** `ghcr.io/rfsbraz/deleterr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/rfsbraz/deleterr/wiki)
- **Issues:** [GitHub Issues](https://github.com/rfsbraz/deleterr/issues)

