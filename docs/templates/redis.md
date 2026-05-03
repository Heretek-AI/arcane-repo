---
title: "Redis"
description: "In-memory data store used as a database, cache, message broker, and streaming engine for high-performance applications"
---

# Redis

In-memory data store used as a database, cache, message broker, and streaming engine for high-performance applications

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/redis/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/redis/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/redis/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `redis` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8e87ebd8f8237ed54885bfe973672791834d2be36434ac55ce2e81eb070c7d08` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `redis` | docker.io/redislabs/redis:latest | Main application service |
| `redis_data` | (volume) | Persistent data storage |

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
| `REDIS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs redis
```

**Port conflict:**
Edit `.env` and change `REDIS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec redis ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect redis --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v redis_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/redis-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/redislabs/redis:latest`

