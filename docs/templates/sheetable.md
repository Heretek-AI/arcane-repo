---
title: "Sheetable"
description: "Self-hosted Sheetable deployment via Docker"
---

# Sheetable

Self-hosted Sheetable deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sheetable/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sheetable/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sheetable/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sheetable` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3527935119319e095a5b8cb3e8a041e334bb5de5a7db145822d9a12c66645927` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `sheetable` | ghcr.io/sheetable/sheetable:latest | Main application service |
| `sheetable_data` | (volume) | Persistent data storage |

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
| `SHEETABLE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs sheetable
```

**Port conflict:**
Edit `.env` and change `SHEETABLE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec sheetable ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect sheetable --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v sheetable_data:/data -v $(pwd):/backup alpine tar czf /backup/sheetable-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v sheetable_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/sheetable-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Sheetable](https://github.com/sheetable/sheetable)
- **Docker Image:** `ghcr.io/sheetable/sheetable:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sheetable/sheetable/wiki)
- **Issues:** [GitHub Issues](https://github.com/sheetable/sheetable/issues)

