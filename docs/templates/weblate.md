---
title: "Weblate"
description: "Self-hosted Weblate deployment via Docker"
---

# Weblate

Self-hosted Weblate deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/weblate/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/weblate/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/weblate/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `weblate` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `60bf174423477e5834edbfd4d40750800a8e00ae2caea73974ef305bcb56b43f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `weblate` | docker.io/weblate/weblate:latest | Main application service |
| `weblate_data` | (volume) | Persistent data storage |

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
| `WEBLATE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs weblate
```

**Port conflict:**
Edit `.env` and change `WEBLATE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec weblate ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect weblate --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v weblate_data:/data -v $(pwd):/backup alpine tar czf /backup/weblate-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v weblate_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/weblate-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Weblate](https://github.com/weblate/weblate)
- **Docker Image:** `docker.io/weblate/weblate:latest`
- **Documentation:** [GitHub Wiki](https://github.com/weblate/weblate/wiki)
- **Issues:** [GitHub Issues](https://github.com/weblate/weblate/issues)

