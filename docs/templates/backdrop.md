---
title: "Backdrop"
description: "Self-hosted Backdrop deployment via Docker"
---

# Backdrop

Self-hosted Backdrop deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/backdrop/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/backdrop/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/backdrop/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `backdrop` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b0e5fd4ce57c3e9b7f1a624c7ddddf363bee26a11a7aca3cbf2f19235286aa8c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `backdrop` | docker.io/library/backdrop:latest | Main application service |
| `backdrop_data` | (volume) | Persistent data storage |

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
| `BACKDROP_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs backdrop
```

**Port conflict:**
Edit `.env` and change `BACKDROP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec backdrop ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect backdrop --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v backdrop_data:/data -v $(pwd):/backup alpine tar czf /backup/backdrop-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v backdrop_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/backdrop-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/library/backdrop:latest`

