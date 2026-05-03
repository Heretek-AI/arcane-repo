---
title: "Filestash"
description: "Self-hosted Filestash deployment via Docker"
---

# Filestash

Self-hosted Filestash deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/storage" class="tag-badge">storage</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/filestash/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/filestash/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/filestash/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `filestash` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `12a9bd9b97a0e5b9cd1ba99b6582387837580f03ce47d5f6fde4768d3817f7af` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `filestash` | docker.io/machines/filestash:latest | Main application service |
| `filestash_data` | (volume) | Persistent data storage |

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
| `FILESTASH_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs filestash
```

**Port conflict:**
Edit `.env` and change `FILESTASH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec filestash ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect filestash --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v filestash_data:/data -v $(pwd):/backup alpine tar czf /backup/filestash-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v filestash_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/filestash-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Filestash](https://github.com/machines/filestash)
- **Docker Image:** `docker.io/machines/filestash:latest`
- **Documentation:** [GitHub Wiki](https://github.com/machines/filestash/wiki)
- **Issues:** [GitHub Issues](https://github.com/machines/filestash/issues)

