---
title: "Firefly Iii"
description: "Self-hosted Firefly Iii deployment via Docker"
---

# Firefly Iii

Self-hosted Firefly Iii deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/firefly-iii/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/firefly-iii/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/firefly-iii/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `firefly-iii` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `635382415b6131608422d8d0cb8de488dd6c7f2a5d76b2aad693f8d2991eb7f3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `firefly-iii` | ghcr.io/supersandro2000/firefly-iii:latest | Main application service |
| `firefly-iii_data` | (volume) | Persistent data storage |

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
| `FIREFLY_III_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs firefly-iii
```

**Port conflict:**
Edit `.env` and change `FIREFLY-III_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec firefly-iii ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect firefly-iii --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v firefly-iii_data:/data -v $(pwd):/backup alpine tar czf /backup/firefly-iii-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v firefly-iii_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/firefly-iii-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Firefly Iii](https://github.com/supersandro2000/firefly-iii)
- **Docker Image:** `ghcr.io/supersandro2000/firefly-iii:latest`
- **Documentation:** [GitHub Wiki](https://github.com/supersandro2000/firefly-iii/wiki)
- **Issues:** [GitHub Issues](https://github.com/supersandro2000/firefly-iii/issues)

