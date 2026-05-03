---
title: "Domain Locker"
description: "Self-hosted Domain Locker deployment via Docker"
---

# Domain Locker

Self-hosted Domain Locker deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/domain-locker/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/domain-locker/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/domain-locker/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `domain-locker` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `550d74e0a13b5141824720d9968d2899cf8bbd81ad91435dfe283125ad5fb273` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `domain-locker` | ghcr.io/lissy93/domain-locker:latest | Main application service |
| `domain-locker_data` | (volume) | Persistent data storage |

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
| `DOMAIN_LOCKER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs domain-locker
```

**Port conflict:**
Edit `.env` and change `DOMAIN-LOCKER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec domain-locker ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect domain-locker --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v domain-locker_data:/data -v $(pwd):/backup alpine tar czf /backup/domain-locker-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v domain-locker_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/domain-locker-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Domain Locker](https://github.com/lissy93/domain-locker)
- **Docker Image:** `ghcr.io/lissy93/domain-locker:latest`
- **Documentation:** [GitHub Wiki](https://github.com/lissy93/domain-locker/wiki)
- **Issues:** [GitHub Issues](https://github.com/lissy93/domain-locker/issues)

