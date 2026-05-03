---
title: "Strix"
description: "Self-hosted Strix deployment via Docker"
---

# Strix

Self-hosted Strix deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/strix/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/strix/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/strix/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `strix` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `0e5a05b202fc446c0d059b8b34498143a22dff3041acb287ea80afadbc14ce83` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `strix` | docker.io/eduard256/strix:latest | Main application service |
| `strix_data` | (volume) | Persistent data storage |

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
| `STRIX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs strix
```

**Port conflict:**
Edit `.env` and change `STRIX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec strix ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect strix --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v strix_data:/data -v $(pwd):/backup alpine tar czf /backup/strix-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v strix_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/strix-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Strix](https://github.com/eduard256/strix)
- **Docker Image:** `docker.io/eduard256/strix:latest`
- **Documentation:** [GitHub Wiki](https://github.com/eduard256/strix/wiki)
- **Issues:** [GitHub Issues](https://github.com/eduard256/strix/issues)

