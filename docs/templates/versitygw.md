---
title: "Versitygw"
description: "Self-hosted Versitygw deployment via Docker"
---

# Versitygw

Self-hosted Versitygw deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/versitygw/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/versitygw/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/versitygw/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `versitygw` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a521efbf0fad3a8f1cd5c2f8e3f1e6be139c3c1152eff93da658caeafe99defe` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `versitygw` | ghcr.io/versity/versitygw:latest | Main application service |
| `versitygw_data` | (volume) | Persistent data storage |

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
| `VERSITYGW_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs versitygw
```

**Port conflict:**
Edit `.env` and change `VERSITYGW_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec versitygw ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect versitygw --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v versitygw_data:/data -v $(pwd):/backup alpine tar czf /backup/versitygw-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v versitygw_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/versitygw-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Versitygw](https://github.com/versity/versitygw)
- **Docker Image:** `ghcr.io/versity/versitygw:latest`
- **Documentation:** [GitHub Wiki](https://github.com/versity/versitygw/wiki)
- **Issues:** [GitHub Issues](https://github.com/versity/versitygw/issues)

