---
title: "Ampache"
description: "Self-hosted Ampache deployment via Docker"
---

# Ampache

Self-hosted Ampache deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ampache/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ampache/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ampache/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ampache` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `42e546e9de268f21ef76f4285c930ca9a892a012cf3da63edc3ae337e80b162d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ampache` | docker.io/ampache/ampache:latest | Main application service |
| `ampache_data` | (volume) | Persistent data storage |

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
| `AMPACHE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs ampache
```

**Port conflict:**
Edit `.env` and change `AMPACHE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ampache ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ampache --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ampache_data:/data -v $(pwd):/backup alpine tar czf /backup/ampache-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ampache_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ampache-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Ampache](https://github.com/ampache/ampache)
- **Docker Image:** `docker.io/ampache/ampache:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ampache/ampache/wiki)
- **Issues:** [GitHub Issues](https://github.com/ampache/ampache/issues)

