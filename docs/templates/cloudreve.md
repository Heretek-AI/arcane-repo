---
title: "Cloudreve"
description: "Self-hosted Cloudreve deployment via Docker"
---

# Cloudreve

Self-hosted Cloudreve deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cloudreve/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cloudreve/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cloudreve/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cloudreve` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `55f3fe8004b82c6c60bb5f5fd68833a2c9302f1dbbc40f43e093f5197a9c1ad2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cloudreve` | docker.io/cloudreve/cloudreve:latest | Main application service |
| `cloudreve_data` | (volume) | Persistent data storage |

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
| `CLOUDREVE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cloudreve
```

**Port conflict:**
Edit `.env` and change `CLOUDREVE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cloudreve ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cloudreve --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cloudreve_data:/data -v $(pwd):/backup alpine tar czf /backup/cloudreve-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cloudreve_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cloudreve-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cloudreve](https://github.com/cloudreve/cloudreve)
- **Docker Image:** `docker.io/cloudreve/cloudreve:latest`
- **Documentation:** [GitHub Wiki](https://github.com/cloudreve/cloudreve/wiki)
- **Issues:** [GitHub Issues](https://github.com/cloudreve/cloudreve/issues)

