---
title: "Openobserve"
description: "Self-hosted Openobserve deployment via Docker"
---

# Openobserve

Self-hosted Openobserve deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openobserve/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openobserve/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openobserve/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openobserve` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `bd8c584057e223dd25f79a6a7dd75bdcf0f14b08ce8bb02f95875d7dbe18d97f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `openobserve` | docker.io/openobserve/openobserve:latest | Main application service |
| `openobserve_data` | (volume) | Persistent data storage |

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
| `OPENOBSERVE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs openobserve
```

**Port conflict:**
Edit `.env` and change `OPENOBSERVE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec openobserve ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect openobserve --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v openobserve_data:/data -v $(pwd):/backup alpine tar czf /backup/openobserve-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v openobserve_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/openobserve-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Openobserve](https://github.com/openobserve/openobserve)
- **Docker Image:** `docker.io/openobserve/openobserve:latest`
- **Documentation:** [GitHub Wiki](https://github.com/openobserve/openobserve/wiki)
- **Issues:** [GitHub Issues](https://github.com/openobserve/openobserve/issues)

