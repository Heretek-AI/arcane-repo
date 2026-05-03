---
title: "Monetr"
description: "Self-hosted Monetr deployment via Docker"
---

# Monetr

Self-hosted Monetr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/monetr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/monetr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/monetr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `monetr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ad99b78d65ff377ee5ce862da846ac27e1708b9066e1f2a595fc3d18be1d020e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `monetr` | ghcr.io/monetr/monetr:latest | Main application service |
| `monetr_data` | (volume) | Persistent data storage |

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
| `MONETR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs monetr
```

**Port conflict:**
Edit `.env` and change `MONETR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec monetr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect monetr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v monetr_data:/data -v $(pwd):/backup alpine tar czf /backup/monetr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v monetr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/monetr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Monetr](https://github.com/monetr/monetr)
- **Docker Image:** `ghcr.io/monetr/monetr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/monetr/monetr/wiki)
- **Issues:** [GitHub Issues](https://github.com/monetr/monetr/issues)

