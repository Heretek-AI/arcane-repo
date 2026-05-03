---
title: "Beets"
description: "Self-hosted Beets deployment via Docker"
---

# Beets

Self-hosted Beets deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beets/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beets/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/beets/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `beets` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e28bf0e23dba085b84171fb8ca833667e2a69899f375a313f818a2cd84b46138` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `beets` | ghcr.io/linuxserver/beets:latest | Main application service |
| `beets_data` | (volume) | Persistent data storage |

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
| `BEETS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs beets
```

**Port conflict:**
Edit `.env` and change `BEETS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec beets ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect beets --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v beets_data:/data -v $(pwd):/backup alpine tar czf /backup/beets-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v beets_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/beets-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Beets](https://github.com/linuxserver/beets)
- **Docker Image:** `ghcr.io/linuxserver/beets:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/beets/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/beets/issues)

