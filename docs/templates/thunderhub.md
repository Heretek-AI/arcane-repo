---
title: "Thunderhub"
description: "Self-hosted Thunderhub deployment via Docker"
---

# Thunderhub

Self-hosted Thunderhub deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/thunderhub/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/thunderhub/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/thunderhub/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `thunderhub` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `85cab4ed777ae6536f9fdfcf1b26bebd049c38ee1af1e2a35ee098967662adf0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `thunderhub` | docker.io/apotdevin/thunderhub:latest | Main application service |
| `thunderhub_data` | (volume) | Persistent data storage |

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
| `THUNDERHUB_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs thunderhub
```

**Port conflict:**
Edit `.env` and change `THUNDERHUB_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec thunderhub ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect thunderhub --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v thunderhub_data:/data -v $(pwd):/backup alpine tar czf /backup/thunderhub-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v thunderhub_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/thunderhub-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Thunderhub](https://github.com/apotdevin/thunderhub)
- **Docker Image:** `docker.io/apotdevin/thunderhub:latest`
- **Documentation:** [GitHub Wiki](https://github.com/apotdevin/thunderhub/wiki)
- **Issues:** [GitHub Issues](https://github.com/apotdevin/thunderhub/issues)

