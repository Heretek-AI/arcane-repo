---
title: "Docsify"
description: "Self-hosted Docsify deployment via Docker"
---

# Docsify

Self-hosted Docsify deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docsify/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docsify/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docsify/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `docsify` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `db5fb746ea9a499f7e6e559c40efdaa01c996727020af6701135580876af17a3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `docsify` | ghcr.io/sujaykumarh/docsify:latest | Main application service |
| `docsify_data` | (volume) | Persistent data storage |

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
| `DOCSIFY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs docsify
```

**Port conflict:**
Edit `.env` and change `DOCSIFY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec docsify ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect docsify --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v docsify_data:/data -v $(pwd):/backup alpine tar czf /backup/docsify-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v docsify_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/docsify-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Docsify](https://github.com/sujaykumarh/docsify)
- **Docker Image:** `ghcr.io/sujaykumarh/docsify:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sujaykumarh/docsify/wiki)
- **Issues:** [GitHub Issues](https://github.com/sujaykumarh/docsify/issues)

