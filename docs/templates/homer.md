---
title: "Homer"
description: "Self-hosted Homer deployment via Docker"
---

# Homer

Self-hosted Homer deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homer/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homer/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homer/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `homer` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dd2f044b86a3e140621a6081fb62e8ccc2d2d8bf9e6dcfb5da492667d3aae7ff` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `homer` | docker.io/b4bz/homer:latest | Main application service |
| `homer_data` | (volume) | Persistent data storage |

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
| `HOMER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs homer
```

**Port conflict:**
Edit `.env` and change `HOMER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec homer ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect homer --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v homer_data:/data -v $(pwd):/backup alpine tar czf /backup/homer-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v homer_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/homer-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Homer](https://github.com/b4bz/homer)
- **Docker Image:** `docker.io/b4bz/homer:latest`
- **Documentation:** [GitHub Wiki](https://github.com/b4bz/homer/wiki)
- **Issues:** [GitHub Issues](https://github.com/b4bz/homer/issues)

