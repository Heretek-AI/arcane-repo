---
title: "Reiverr"
description: "Self-hosted Reiverr deployment via Docker"
---

# Reiverr

Self-hosted Reiverr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/reiverr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/reiverr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/reiverr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `reiverr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d7f80ae531c8f41a711cb29ad22c076e145cd905d0f1532d0a54d5585afe7ff9` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `reiverr` | docker.io/t0bis/reiverr:latest | Main application service |
| `reiverr_data` | (volume) | Persistent data storage |

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
| `REIVERR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs reiverr
```

**Port conflict:**
Edit `.env` and change `REIVERR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec reiverr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect reiverr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v reiverr_data:/data -v $(pwd):/backup alpine tar czf /backup/reiverr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v reiverr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/reiverr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Reiverr](https://github.com/t0bis/reiverr)
- **Docker Image:** `docker.io/t0bis/reiverr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/t0bis/reiverr/wiki)
- **Issues:** [GitHub Issues](https://github.com/t0bis/reiverr/issues)

