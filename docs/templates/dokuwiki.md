---
title: "Dokuwiki"
description: "Self-hosted Dokuwiki deployment via Docker"
---

# Dokuwiki

Self-hosted Dokuwiki deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokuwiki/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokuwiki/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dokuwiki/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dokuwiki` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `fb2317a90a4ae5a0d72a36b204f8b28569981f84e5e95853b56975c285cabbc1` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dokuwiki` | ghcr.io/dokuwiki/dokuwiki:latest | Main application service |
| `dokuwiki_data` | (volume) | Persistent data storage |

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
| `DOKUWIKI_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dokuwiki
```

**Port conflict:**
Edit `.env` and change `DOKUWIKI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dokuwiki ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dokuwiki --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dokuwiki_data:/data -v $(pwd):/backup alpine tar czf /backup/dokuwiki-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dokuwiki_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dokuwiki-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dokuwiki](https://github.com/dokuwiki/dokuwiki)
- **Docker Image:** `ghcr.io/dokuwiki/dokuwiki:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dokuwiki/dokuwiki/wiki)
- **Issues:** [GitHub Issues](https://github.com/dokuwiki/dokuwiki/issues)

