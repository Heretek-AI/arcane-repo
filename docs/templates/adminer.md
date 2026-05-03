---
title: "Adminer"
description: "Self-hosted Adminer deployment via Docker"
---

# Adminer

Self-hosted Adminer deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/adminer/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/adminer/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/adminer/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `adminer` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f67c38274ae64cfe6aebfd3a89c1aa6e7695f650ae15106a3bb9a5780c717ffb` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `adminer` | docker.io/library/adminer:latest | Main application service |
| `adminer_data` | (volume) | Persistent data storage |

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
| `ADMINER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs adminer
```

**Port conflict:**
Edit `.env` and change `ADMINER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec adminer ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect adminer --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v adminer_data:/data -v $(pwd):/backup alpine tar czf /backup/adminer-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v adminer_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/adminer-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/library/adminer:latest`

