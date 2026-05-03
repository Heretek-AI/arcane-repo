---
title: "Pyinventory"
description: "Self-hosted Pyinventory deployment via Docker"
---

# Pyinventory

Self-hosted Pyinventory deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pyinventory/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pyinventory/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pyinventory/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pyinventory` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `baa8ac08d630e8706dd783cd715282d75b112d2a8e11f8480a3f66e12cedface` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pyinventory` | ghcr.io/korylprince/pyinventory:latest | Main application service |
| `pyinventory_data` | (volume) | Persistent data storage |

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
| `PYINVENTORY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pyinventory
```

**Port conflict:**
Edit `.env` and change `PYINVENTORY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pyinventory ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pyinventory --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pyinventory_data:/data -v $(pwd):/backup alpine tar czf /backup/pyinventory-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pyinventory_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pyinventory-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pyinventory](https://github.com/korylprince/pyinventory)
- **Docker Image:** `ghcr.io/korylprince/pyinventory:latest`
- **Documentation:** [GitHub Wiki](https://github.com/korylprince/pyinventory/wiki)
- **Issues:** [GitHub Issues](https://github.com/korylprince/pyinventory/issues)

