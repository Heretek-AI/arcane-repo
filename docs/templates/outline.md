---
title: "Outline"
description: "Self-hosted Outline deployment via Docker"
---

# Outline

Self-hosted Outline deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/outline/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/outline/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/outline/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `outline` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `bb432eed5262dc2e4713efa945276920b4e7aaf5baa32af37085edd6fb92799d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `outline` | docker.io/outlinewiki/outline:latest | Main application service |
| `outline_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:3000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OUTLINE_PORT` | `3000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs outline
```

**Port conflict:**
Edit `.env` and change `OUTLINE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec outline ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect outline --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v outline_data:/data -v $(pwd):/backup alpine tar czf /backup/outline-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v outline_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/outline-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Outline](https://github.com/outlinewiki/outline)
- **Docker Image:** `docker.io/outlinewiki/outline:latest`
- **Documentation:** [GitHub Wiki](https://github.com/outlinewiki/outline/wiki)
- **Issues:** [GitHub Issues](https://github.com/outlinewiki/outline/issues)

