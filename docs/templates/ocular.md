---
title: "Ocular"
description: "Self-hosted Ocular deployment via Docker"
---

# Ocular

Self-hosted Ocular deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ocular/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ocular/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ocular/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ocular` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5d0c424169a0b6243f689e010b81548f0288bc0e56f596d780f94af5556cf01a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ocular` | docker.io/daksharma05/ocular:latest | Main application service |
| `ocular_data` | (volume) | Persistent data storage |

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
| `OCULAR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs ocular
```

**Port conflict:**
Edit `.env` and change `OCULAR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ocular ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ocular --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ocular_data:/data -v $(pwd):/backup alpine tar czf /backup/ocular-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ocular_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ocular-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Ocular](https://github.com/daksharma05/ocular)
- **Docker Image:** `docker.io/daksharma05/ocular:latest`
- **Documentation:** [GitHub Wiki](https://github.com/daksharma05/ocular/wiki)
- **Issues:** [GitHub Issues](https://github.com/daksharma05/ocular/issues)

