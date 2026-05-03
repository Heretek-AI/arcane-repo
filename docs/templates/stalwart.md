---
title: "Stalwart"
description: "Self-hosted Stalwart deployment via Docker"
---

# Stalwart

Self-hosted Stalwart deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/stalwart/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/stalwart/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/stalwart/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `stalwart` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6bfcf2d773afc67c99256adfa727d0506edb9beb6d81cedee47616b64b554b31` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `stalwart` | ghcr.io/stalwartlabs/stalwart:latest | Main application service |
| `stalwart_data` | (volume) | Persistent data storage |

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
| `STALWART_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs stalwart
```

**Port conflict:**
Edit `.env` and change `STALWART_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec stalwart ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect stalwart --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v stalwart_data:/data -v $(pwd):/backup alpine tar czf /backup/stalwart-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v stalwart_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/stalwart-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Stalwart](https://github.com/stalwartlabs/stalwart)
- **Docker Image:** `ghcr.io/stalwartlabs/stalwart:latest`
- **Documentation:** [GitHub Wiki](https://github.com/stalwartlabs/stalwart/wiki)
- **Issues:** [GitHub Issues](https://github.com/stalwartlabs/stalwart/issues)

