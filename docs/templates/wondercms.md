---
title: "Wondercms"
description: "Self-hosted Wondercms deployment via Docker"
---

# Wondercms

Self-hosted Wondercms deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wondercms/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wondercms/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wondercms/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `wondercms` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `fb30ebbdd81c3b4b237d3408446d3f1e626ca9d9c4bffe5ac357288240e1af54` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `wondercms` | docker.io/mablanco/wondercms:latest | Main application service |
| `wondercms_data` | (volume) | Persistent data storage |

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
| `WONDERCMS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs wondercms
```

**Port conflict:**
Edit `.env` and change `WONDERCMS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec wondercms ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect wondercms --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v wondercms_data:/data -v $(pwd):/backup alpine tar czf /backup/wondercms-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v wondercms_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/wondercms-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Wondercms](https://github.com/mablanco/wondercms)
- **Docker Image:** `docker.io/mablanco/wondercms:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mablanco/wondercms/wiki)
- **Issues:** [GitHub Issues](https://github.com/mablanco/wondercms/issues)

