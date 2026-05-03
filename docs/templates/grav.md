---
title: "Grav"
description: "Self-hosted Grav deployment via Docker"
---

# Grav

Self-hosted Grav deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grav/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grav/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grav/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `grav` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b9024fefd36b852ba3a5123cac8f55701e19820ae938ef272fdfda6ccc94dda7` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `grav` | ghcr.io/linuxserver/grav:latest | Main application service |
| `grav_data` | (volume) | Persistent data storage |

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
| `GRAV_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs grav
```

**Port conflict:**
Edit `.env` and change `GRAV_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec grav ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect grav --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v grav_data:/data -v $(pwd):/backup alpine tar czf /backup/grav-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v grav_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/grav-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Grav](https://github.com/linuxserver/grav)
- **Docker Image:** `ghcr.io/linuxserver/grav:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/grav/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/grav/issues)

