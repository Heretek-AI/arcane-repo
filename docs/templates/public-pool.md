---
title: "Public Pool"
description: "Self-hosted Public Pool deployment via Docker"
---

# Public Pool

Self-hosted Public Pool deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/public-pool/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/public-pool/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/public-pool/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `public-pool` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3eb6fdca447d9a8ffdaf56f0b7901f3d274ed9e1bdbecf0a2c6e6a37bb9cc80c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `public-pool` | ghcr.io/sethforprivacy/public-pool:latest | Main application service |
| `public-pool_data` | (volume) | Persistent data storage |

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
| `PUBLIC_POOL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs public-pool
```

**Port conflict:**
Edit `.env` and change `PUBLIC-POOL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec public-pool ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect public-pool --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v public-pool_data:/data -v $(pwd):/backup alpine tar czf /backup/public-pool-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v public-pool_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/public-pool-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Public Pool](https://github.com/sethforprivacy/public-pool)
- **Docker Image:** `ghcr.io/sethforprivacy/public-pool:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sethforprivacy/public-pool/wiki)
- **Issues:** [GitHub Issues](https://github.com/sethforprivacy/public-pool/issues)

