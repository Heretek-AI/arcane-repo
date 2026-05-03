---
title: "Grocy"
description: "Self-hosted Grocy deployment via Docker"
---

# Grocy

Self-hosted Grocy deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grocy/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grocy/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grocy/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `grocy` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `73ffc8a6c8efc6dcdc2ce29cd21c2a8627591891b9c627346c156bf3f952f644` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `grocy` | ghcr.io/linuxserver/grocy:latest | Main application service |
| `grocy_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:80/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:80](http://localhost:80) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `GROCY_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs grocy
```

**Port conflict:**
Edit `.env` and change `GROCY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec grocy ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect grocy --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v grocy_data:/data -v $(pwd):/backup alpine tar czf /backup/grocy-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v grocy_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/grocy-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Grocy](https://github.com/linuxserver/grocy)
- **Docker Image:** `ghcr.io/linuxserver/grocy:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/grocy/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/grocy/issues)

