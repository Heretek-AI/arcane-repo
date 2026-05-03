---
title: "Wikidocs"
description: "Self-hosted Wikidocs deployment via Docker"
---

# Wikidocs

Self-hosted Wikidocs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikidocs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikidocs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikidocs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `wikidocs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e28e006ecb6a3f31dea915860583741b20544687676ae852859ddff0d7014ec6` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `wikidocs` | docker.io/zavy86/wikidocs:latest | Main application service |
| `wikidocs_data` | (volume) | Persistent data storage |

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
| `WIKIDOCS_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs wikidocs
```

**Port conflict:**
Edit `.env` and change `WIKIDOCS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec wikidocs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect wikidocs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v wikidocs_data:/data -v $(pwd):/backup alpine tar czf /backup/wikidocs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v wikidocs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/wikidocs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Wikidocs](https://github.com/zavy86/wikidocs)
- **Docker Image:** `docker.io/zavy86/wikidocs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/zavy86/wikidocs/wiki)
- **Issues:** [GitHub Issues](https://github.com/zavy86/wikidocs/issues)

