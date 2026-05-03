---
title: "Headscale"
description: "Self-hosted Headscale deployment via Docker"
---

# Headscale

Self-hosted Headscale deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/headscale/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/headscale/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/headscale/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `headscale` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a27a8b248c0dd29d2b0be7bc3f622a3f75f6982d326474b99c8475a40cebe817` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `headscale` | docker.io/headscale/headscale:latest | Main application service |
| `headscale_data` | (volume) | Persistent data storage |

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
| `HEADSCALE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs headscale
```

**Port conflict:**
Edit `.env` and change `HEADSCALE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec headscale ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect headscale --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v headscale_data:/data -v $(pwd):/backup alpine tar czf /backup/headscale-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v headscale_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/headscale-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Headscale](https://github.com/headscale/headscale)
- **Docker Image:** `docker.io/headscale/headscale:latest`
- **Documentation:** [GitHub Wiki](https://github.com/headscale/headscale/wiki)
- **Issues:** [GitHub Issues](https://github.com/headscale/headscale/issues)

