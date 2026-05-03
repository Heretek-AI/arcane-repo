---
title: "Pollaris"
description: "Self-hosted Pollaris deployment via Docker"
---

# Pollaris

Self-hosted Pollaris deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pollaris/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pollaris/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pollaris/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pollaris` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `31856ba63d3a410eeeaf95b24dcac8b831370892b28a51c0a67668abeb4091f6` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pollaris` | docker.io/linusll/pollaris:latest | Main application service |
| `pollaris_data` | (volume) | Persistent data storage |

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
| `POLLARIS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pollaris
```

**Port conflict:**
Edit `.env` and change `POLLARIS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pollaris ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pollaris --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pollaris_data:/data -v $(pwd):/backup alpine tar czf /backup/pollaris-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pollaris_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pollaris-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pollaris](https://github.com/linusll/pollaris)
- **Docker Image:** `docker.io/linusll/pollaris:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linusll/pollaris/wiki)
- **Issues:** [GitHub Issues](https://github.com/linusll/pollaris/issues)

