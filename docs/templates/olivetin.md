---
title: "Olivetin"
description: "Self-hosted Olivetin deployment via Docker"
---

# Olivetin

Self-hosted Olivetin deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/olivetin/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/olivetin/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/olivetin/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `olivetin` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `06accd713d305b88e455a53c7a705de4768e283d05c1fb9a8dd5e172e5664eb0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `olivetin` | ghcr.io/olivetin/olivetin:latest | Main application service |
| `olivetin_data` | (volume) | Persistent data storage |

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
| `OLIVETIN_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs olivetin
```

**Port conflict:**
Edit `.env` and change `OLIVETIN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec olivetin ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect olivetin --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v olivetin_data:/data -v $(pwd):/backup alpine tar czf /backup/olivetin-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v olivetin_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/olivetin-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Olivetin](https://github.com/olivetin/olivetin)
- **Docker Image:** `ghcr.io/olivetin/olivetin:latest`
- **Documentation:** [GitHub Wiki](https://github.com/olivetin/olivetin/wiki)
- **Issues:** [GitHub Issues](https://github.com/olivetin/olivetin/issues)

