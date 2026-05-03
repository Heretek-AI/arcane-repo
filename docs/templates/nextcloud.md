---
title: "Nextcloud"
description: "Self-hosted content collaboration platform with file sync, calendar, contacts, and extensive app ecosystem"
---

# Nextcloud

Self-hosted content collaboration platform with file sync, calendar, contacts, and extensive app ecosystem

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nextcloud/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nextcloud/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nextcloud/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `nextcloud` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b1c6817ff30510c7ec083406b140f54270f91a694a0fbce2ae91ac42080ab003` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `nextcloud` | docker.io/library/nextcloud:latest | Main application service |
| `nextcloud_data` | (volume) | Persistent data storage |

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
| `NEXTCLOUD_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs nextcloud
```

**Port conflict:**
Edit `.env` and change `NEXTCLOUD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec nextcloud ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect nextcloud --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v nextcloud_data:/data -v $(pwd):/backup alpine tar czf /backup/nextcloud-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v nextcloud_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/nextcloud-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/library/nextcloud:latest`

