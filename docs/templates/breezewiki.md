---
title: "Breezewiki"
description: "Self-hosted Breezewiki deployment via Docker"
---

# Breezewiki

Self-hosted Breezewiki deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/breezewiki/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/breezewiki/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/breezewiki/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `breezewiki` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `98ef6d9e0e75c4fff087673dbe7b08bc114bc827aec695baf44d3f9073bb067f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `breezewiki` | ghcr.io/fariszr/breezewiki:latest | Main application service |
| `breezewiki_data` | (volume) | Persistent data storage |

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
| `BREEZEWIKI_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs breezewiki
```

**Port conflict:**
Edit `.env` and change `BREEZEWIKI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec breezewiki ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect breezewiki --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v breezewiki_data:/data -v $(pwd):/backup alpine tar czf /backup/breezewiki-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v breezewiki_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/breezewiki-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Breezewiki](https://github.com/fariszr/breezewiki)
- **Docker Image:** `ghcr.io/fariszr/breezewiki:latest`
- **Documentation:** [GitHub Wiki](https://github.com/fariszr/breezewiki/wiki)
- **Issues:** [GitHub Issues](https://github.com/fariszr/breezewiki/issues)

