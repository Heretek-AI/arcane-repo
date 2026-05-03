---
title: "Otter Wiki"
description: "Self-hosted Otter Wiki deployment via Docker"
---

# Otter Wiki

Self-hosted Otter Wiki deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/otter-wiki/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/otter-wiki/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/otter-wiki/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `otter-wiki` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ce0084b13d0cf0bbefa6bd7902fc7ec8948c5f502afcc62527167ef5d3d29af5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `otter-wiki` | docker.io/redimp/otterwiki:latest | Main application service |
| `otter-wiki_data` | (volume) | Persistent data storage |

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
| `OTTER_WIKI_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs otter-wiki
```

**Port conflict:**
Edit `.env` and change `OTTER-WIKI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec otter-wiki ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect otter-wiki --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v otter-wiki_data:/data -v $(pwd):/backup alpine tar czf /backup/otter-wiki-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v otter-wiki_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/otter-wiki-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Otter Wiki](https://github.com/redimp/otterwiki)
- **Docker Image:** `docker.io/redimp/otterwiki:latest`
- **Documentation:** [GitHub Wiki](https://github.com/redimp/otterwiki/wiki)
- **Issues:** [GitHub Issues](https://github.com/redimp/otterwiki/issues)

