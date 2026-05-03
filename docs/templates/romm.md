---
title: "Romm"
description: "Self-hosted Romm deployment via Docker"
---

# Romm

Self-hosted Romm deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/romm/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/romm/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/romm/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `romm` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c34a4fefba0f9db63a4314556cd7d42640246b481620485c7058baca51204c90` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `romm` | ghcr.io/rommapp/romm:latest | Main application service |
| `romm_data` | (volume) | Persistent data storage |

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
| `ROMM_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs romm
```

**Port conflict:**
Edit `.env` and change `ROMM_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec romm ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect romm --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v romm_data:/data -v $(pwd):/backup alpine tar czf /backup/romm-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v romm_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/romm-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Romm](https://github.com/rommapp/romm)
- **Docker Image:** `ghcr.io/rommapp/romm:latest`
- **Documentation:** [GitHub Wiki](https://github.com/rommapp/romm/wiki)
- **Issues:** [GitHub Issues](https://github.com/rommapp/romm/issues)

