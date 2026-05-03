---
title: "Firefox"
description: "Self-hosted Firefox deployment via Docker"
---

# Firefox

Self-hosted Firefox deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/firefox/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/firefox/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/firefox/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `firefox` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `14b01610aa542300d4d855aed714e8535ab9f98609fc3adf3210c35936178f3a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `firefox` | ghcr.io/jlesage/firefox:latest | Main application service |
| `firefox_data` | (volume) | Persistent data storage |

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
| `FIREFOX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs firefox
```

**Port conflict:**
Edit `.env` and change `FIREFOX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec firefox ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect firefox --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v firefox_data:/data -v $(pwd):/backup alpine tar czf /backup/firefox-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v firefox_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/firefox-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Firefox](https://github.com/jlesage/firefox)
- **Docker Image:** `ghcr.io/jlesage/firefox:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jlesage/firefox/wiki)
- **Issues:** [GitHub Issues](https://github.com/jlesage/firefox/issues)

