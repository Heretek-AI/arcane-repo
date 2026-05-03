---
title: "Metabase"
description: "Self-hosted Metabase deployment via Docker"
---

# Metabase

Self-hosted Metabase deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/metabase/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/metabase/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/metabase/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `metabase` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `2e9651d32a804a36491226fafeb9833bbfd2a3f9d10be60fb38571f2c0a0260f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `metabase` | docker.io/metabase/metabase:latest | Main application service |
| `metabase_data` | (volume) | Persistent data storage |

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
| `METABASE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs metabase
```

**Port conflict:**
Edit `.env` and change `METABASE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec metabase ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect metabase --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v metabase_data:/data -v $(pwd):/backup alpine tar czf /backup/metabase-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v metabase_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/metabase-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Metabase](https://github.com/metabase/metabase)
- **Docker Image:** `docker.io/metabase/metabase:latest`
- **Documentation:** [GitHub Wiki](https://github.com/metabase/metabase/wiki)
- **Issues:** [GitHub Issues](https://github.com/metabase/metabase/issues)

