---
title: "Znc"
description: "Self-hosted Znc deployment via Docker"
---

# Znc

Self-hosted Znc deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/znc/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/znc/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/znc/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `znc` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `37f534f4a5ee8021303d9af133857e5057564c3d6187cdaf1bd706002469aef9` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `znc` | docker.io/library/znc:latest | Main application service |
| `znc_data` | (volume) | Persistent data storage |

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
| `ZNC_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs znc
```

**Port conflict:**
Edit `.env` and change `ZNC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec znc ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect znc --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v znc_data:/data -v $(pwd):/backup alpine tar czf /backup/znc-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v znc_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/znc-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/library/znc:latest`

