---
title: "Musicbrainz"
description: "Self-hosted Musicbrainz deployment via Docker"
---

# Musicbrainz

Self-hosted Musicbrainz deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/musicbrainz/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/musicbrainz/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/musicbrainz/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `musicbrainz` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `507c8c8102d988b8555d70593c42393980c19b685479c94da4cf9d9f1f41ab1f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `musicbrainz` | ghcr.io/linuxserver/musicbrainz:latest | Main application service |
| `musicbrainz_data` | (volume) | Persistent data storage |

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
| `MUSICBRAINZ_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs musicbrainz
```

**Port conflict:**
Edit `.env` and change `MUSICBRAINZ_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec musicbrainz ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect musicbrainz --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v musicbrainz_data:/data -v $(pwd):/backup alpine tar czf /backup/musicbrainz-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v musicbrainz_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/musicbrainz-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Musicbrainz](https://github.com/linuxserver/musicbrainz)
- **Docker Image:** `ghcr.io/linuxserver/musicbrainz:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/musicbrainz/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/musicbrainz/issues)

