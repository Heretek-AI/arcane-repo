---
title: "Tautulli"
description: "Self-hosted Tautulli deployment via Docker"
---

# Tautulli

Self-hosted Tautulli deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tautulli/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tautulli/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tautulli/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tautulli` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d80ab785e348fbd21ed267d6640e557462d1a2077201b727c6d2568c43f8be40` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tautulli` | ghcr.io/tautulli/tautulli:latest | Main application service |
| `tautulli_data` | (volume) | Persistent data storage |

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
| `TAUTULLI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tautulli
```

**Port conflict:**
Edit `.env` and change `TAUTULLI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tautulli ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tautulli --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tautulli_data:/data -v $(pwd):/backup alpine tar czf /backup/tautulli-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tautulli_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tautulli-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tautulli](https://github.com/tautulli/tautulli)
- **Docker Image:** `ghcr.io/tautulli/tautulli:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tautulli/tautulli/wiki)
- **Issues:** [GitHub Issues](https://github.com/tautulli/tautulli/issues)

