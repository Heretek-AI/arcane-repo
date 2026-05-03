---
title: "Nodejs"
description: "Self-hosted Nodejs deployment via Docker"
---

# Nodejs

Self-hosted Nodejs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nodejs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nodejs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nodejs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `nodejs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f01d1eb9b00465dc99b4c67f5d94881338538af02d23200652a50867076d67c9` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `nodejs` | docker.io/paketobuildpacks/nodejs:latest | Main application service |
| `nodejs_data` | (volume) | Persistent data storage |

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
| `NODEJS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs nodejs
```

**Port conflict:**
Edit `.env` and change `NODEJS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec nodejs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect nodejs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v nodejs_data:/data -v $(pwd):/backup alpine tar czf /backup/nodejs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v nodejs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/nodejs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Nodejs](https://github.com/paketobuildpacks/nodejs)
- **Docker Image:** `docker.io/paketobuildpacks/nodejs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/paketobuildpacks/nodejs/wiki)
- **Issues:** [GitHub Issues](https://github.com/paketobuildpacks/nodejs/issues)

