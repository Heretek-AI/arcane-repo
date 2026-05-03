---
title: "Sogo"
description: "Self-hosted Sogo deployment via Docker"
---

# Sogo

Self-hosted Sogo deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sogo/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sogo/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sogo/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sogo` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `88d2a7ddc6be72cc026f6e51259db9d8c298f5e9ab5fd36100c23890ddd2910b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `sogo` | ghcr.io/mailcow/sogo:latest | Main application service |
| `sogo_data` | (volume) | Persistent data storage |

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
| `SOGO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs sogo
```

**Port conflict:**
Edit `.env` and change `SOGO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec sogo ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect sogo --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v sogo_data:/data -v $(pwd):/backup alpine tar czf /backup/sogo-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v sogo_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/sogo-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Sogo](https://github.com/mailcow/sogo)
- **Docker Image:** `ghcr.io/mailcow/sogo:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mailcow/sogo/wiki)
- **Issues:** [GitHub Issues](https://github.com/mailcow/sogo/issues)

