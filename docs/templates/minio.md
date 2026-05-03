---
title: "Minio"
description: "Self-hosted Minio deployment via Docker"
---

# Minio

Self-hosted Minio deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/minio/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/minio/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/minio/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `minio` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e45e9523c0f5c103593881cf71cb1fcaa7ff91bec15f8372b35ac5a316c7d98a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `minio` | docker.io/minio/minio:latest | Main application service |
| `minio_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:9000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9000](http://localhost:9000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MINIO_PORT` | `9000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs minio
```

**Port conflict:**
Edit `.env` and change `MINIO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec minio ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect minio --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v minio_data:/data -v $(pwd):/backup alpine tar czf /backup/minio-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v minio_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/minio-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/minio/minio:latest`

