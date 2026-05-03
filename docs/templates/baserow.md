---
title: "Baserow"
description: "Self-hosted Baserow deployment via Docker"
---

# Baserow

Self-hosted Baserow deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/baserow/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/baserow/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/baserow/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `baserow` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `cbefe5533bdd80e90ff10762b60946564b31e34fea4c4cf674a43faf79bc199c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `baserow` | docker.io/baserow/baserow:latest | Main application service |
| `baserow_data` | (volume) | Persistent data storage |

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
| `BASEROW_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs baserow
```

**Port conflict:**
Edit `.env` and change `BASEROW_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec baserow ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect baserow --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v baserow_data:/data -v $(pwd):/backup alpine tar czf /backup/baserow-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v baserow_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/baserow-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Baserow](https://github.com/baserow/baserow)
- **Docker Image:** `docker.io/baserow/baserow:latest`
- **Documentation:** [GitHub Wiki](https://github.com/baserow/baserow/wiki)
- **Issues:** [GitHub Issues](https://github.com/baserow/baserow/issues)

