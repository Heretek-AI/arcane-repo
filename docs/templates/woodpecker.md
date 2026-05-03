---
title: "Woodpecker"
description: "Self-hosted Woodpecker deployment via Docker"
---

# Woodpecker

Self-hosted Woodpecker deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/woodpecker/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/woodpecker/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/woodpecker/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `woodpecker` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `81a7438402481d492f51b60d4f6cb73ab6c8dbac8228ec1fcd7aa0f61e26ec43` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `woodpecker` | ghcr.io/daemonless/woodpecker:latest | Main application service |
| `woodpecker_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WOODPECKER_PORT` | `8000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs woodpecker
```

**Port conflict:**
Edit `.env` and change `WOODPECKER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec woodpecker ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect woodpecker --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v woodpecker_data:/data -v $(pwd):/backup alpine tar czf /backup/woodpecker-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v woodpecker_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/woodpecker-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Woodpecker](https://github.com/daemonless/woodpecker)
- **Docker Image:** `ghcr.io/daemonless/woodpecker:latest`
- **Documentation:** [GitHub Wiki](https://github.com/daemonless/woodpecker/wiki)
- **Issues:** [GitHub Issues](https://github.com/daemonless/woodpecker/issues)

