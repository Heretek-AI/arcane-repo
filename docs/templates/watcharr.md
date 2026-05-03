---
title: "Watcharr"
description: "Self-hosted Watcharr deployment via Docker"
---

# Watcharr

Self-hosted Watcharr deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/watcharr/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/watcharr/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/watcharr/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `watcharr` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `df386b503ba9a365ea09adc56e8baf448f5896a8215c5977fe05751e0e3af308` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `watcharr` | ghcr.io/sbondco/watcharr:latest | Main application service |
| `watcharr_data` | (volume) | Persistent data storage |

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
| `WATCHARR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs watcharr
```

**Port conflict:**
Edit `.env` and change `WATCHARR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec watcharr ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect watcharr --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v watcharr_data:/data -v $(pwd):/backup alpine tar czf /backup/watcharr-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v watcharr_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/watcharr-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Watcharr](https://github.com/sbondco/watcharr)
- **Docker Image:** `ghcr.io/sbondco/watcharr:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sbondco/watcharr/wiki)
- **Issues:** [GitHub Issues](https://github.com/sbondco/watcharr/issues)

