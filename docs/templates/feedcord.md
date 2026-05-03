---
title: "Feedcord"
description: "Self-hosted Feedcord deployment via Docker"
---

# Feedcord

Self-hosted Feedcord deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/feedcord/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/feedcord/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/feedcord/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `feedcord` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `17fdb98290d4ea84b4d7d264f4cda9a5d32c77841ff133ed425f62fe9e9f08a0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `feedcord` | docker.io/qolors/feedcord:latest | Main application service |
| `feedcord_data` | (volume) | Persistent data storage |

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
| `FEEDCORD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs feedcord
```

**Port conflict:**
Edit `.env` and change `FEEDCORD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec feedcord ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect feedcord --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v feedcord_data:/data -v $(pwd):/backup alpine tar czf /backup/feedcord-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v feedcord_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/feedcord-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Feedcord](https://github.com/qolors/feedcord)
- **Docker Image:** `docker.io/qolors/feedcord:latest`
- **Documentation:** [GitHub Wiki](https://github.com/qolors/feedcord/wiki)
- **Issues:** [GitHub Issues](https://github.com/qolors/feedcord/issues)

