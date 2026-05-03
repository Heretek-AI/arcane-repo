---
title: "Spip"
description: "Self-hosted Spip deployment via Docker"
---

# Spip

Self-hosted Spip deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/spip/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/spip/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/spip/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `spip` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6171c6d8bcd1689a179f7ce4b291735952ec85d570626e5d4cdcbe2451874ab3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `spip` | docker.io/ipeos/spip:latest | Main application service |
| `spip_data` | (volume) | Persistent data storage |

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
| `SPIP_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs spip
```

**Port conflict:**
Edit `.env` and change `SPIP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec spip ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect spip --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v spip_data:/data -v $(pwd):/backup alpine tar czf /backup/spip-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v spip_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/spip-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Spip](https://github.com/ipeos/spip)
- **Docker Image:** `docker.io/ipeos/spip:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ipeos/spip/wiki)
- **Issues:** [GitHub Issues](https://github.com/ipeos/spip/issues)

