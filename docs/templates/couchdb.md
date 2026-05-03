---
title: "Couchdb"
description: "Self-hosted Couchdb deployment via Docker"
---

# Couchdb

Self-hosted Couchdb deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/couchdb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/couchdb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/couchdb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `couchdb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `0008463fc5f3ec52a278ca1e85fb46b326d2129fada0fa9e302c8ab10c7ae622` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `couchdb` | docker.io/library/couchdb:latest | Main application service |
| `couchdb_data` | (volume) | Persistent data storage |

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
| `COUCHDB_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs couchdb
```

**Port conflict:**
Edit `.env` and change `COUCHDB_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec couchdb ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect couchdb --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v couchdb_data:/data -v $(pwd):/backup alpine tar czf /backup/couchdb-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v couchdb_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/couchdb-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/library/couchdb:latest`

