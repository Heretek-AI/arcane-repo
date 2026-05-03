---
title: "Pingvin Share"
description: "Self-hosted Pingvin Share deployment via Docker"
---

# Pingvin Share

Self-hosted Pingvin Share deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pingvin-share/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pingvin-share/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pingvin-share/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pingvin-share` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d4b42dc9ec8c1b8171ee97a7bb96647dfbe5a7ed2bdfd4a28edc0a2a445d9b63` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pingvin-share` | ghcr.io/stonith404/pingvin-share:latest | Main application service |
| `pingvin-share_data` | (volume) | Persistent data storage |

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
| `PINGVIN_SHARE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pingvin-share
```

**Port conflict:**
Edit `.env` and change `PINGVIN-SHARE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pingvin-share ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pingvin-share --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pingvin-share_data:/data -v $(pwd):/backup alpine tar czf /backup/pingvin-share-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pingvin-share_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pingvin-share-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pingvin Share](https://github.com/stonith404/pingvin-share)
- **Docker Image:** `ghcr.io/stonith404/pingvin-share:latest`
- **Documentation:** [GitHub Wiki](https://github.com/stonith404/pingvin-share/wiki)
- **Issues:** [GitHub Issues](https://github.com/stonith404/pingvin-share/issues)

