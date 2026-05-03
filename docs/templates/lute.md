---
title: "Lute"
description: "Self-hosted Lute deployment via Docker"
---

# Lute

Self-hosted Lute deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lute/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lute/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lute/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `lute` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6fe39c6925e163ff52873e18388acebbdb22cc4b4a63d638e4d8e1d1f715edd4` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `lute` | docker.io/nachoalthabe/lute:latest | Main application service |
| `lute_data` | (volume) | Persistent data storage |

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
| `LUTE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs lute
```

**Port conflict:**
Edit `.env` and change `LUTE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec lute ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect lute --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v lute_data:/data -v $(pwd):/backup alpine tar czf /backup/lute-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v lute_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/lute-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Lute](https://github.com/nachoalthabe/lute)
- **Docker Image:** `docker.io/nachoalthabe/lute:latest`
- **Documentation:** [GitHub Wiki](https://github.com/nachoalthabe/lute/wiki)
- **Issues:** [GitHub Issues](https://github.com/nachoalthabe/lute/issues)

