---
title: "Mautic"
description: "Self-hosted Mautic deployment via Docker"
---

# Mautic

Self-hosted Mautic deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mautic/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mautic/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mautic/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mautic` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `01c3c2edcf6eb491b76896d63d09a56ea3e4e097672603fd84684643b6ce9e9d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mautic` | docker.io/mautic/mautic:latest | Main application service |
| `mautic_data` | (volume) | Persistent data storage |

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
| `MAUTIC_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mautic
```

**Port conflict:**
Edit `.env` and change `MAUTIC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mautic ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mautic --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mautic_data:/data -v $(pwd):/backup alpine tar czf /backup/mautic-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mautic_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mautic-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mautic](https://github.com/mautic/mautic)
- **Docker Image:** `docker.io/mautic/mautic:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mautic/mautic/wiki)
- **Issues:** [GitHub Issues](https://github.com/mautic/mautic/issues)

