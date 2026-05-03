---
title: "Open Meteo"
description: "Self-hosted Open Meteo deployment via Docker"
---

# Open Meteo

Self-hosted Open Meteo deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/open-meteo/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/open-meteo/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/open-meteo/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `open-meteo` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d3de5b520c8169a70d085cbec5aa0a5617e3f56ad5fb4baf956c710ced3ef938` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `open-meteo` | ghcr.io/open-meteo/open-meteo:latest | Main application service |
| `open-meteo_data` | (volume) | Persistent data storage |

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
| `OPEN_METEO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs open-meteo
```

**Port conflict:**
Edit `.env` and change `OPEN-METEO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec open-meteo ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect open-meteo --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v open-meteo_data:/data -v $(pwd):/backup alpine tar czf /backup/open-meteo-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v open-meteo_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/open-meteo-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Open Meteo](https://github.com/open-meteo/open-meteo)
- **Docker Image:** `ghcr.io/open-meteo/open-meteo:latest`
- **Documentation:** [GitHub Wiki](https://github.com/open-meteo/open-meteo/wiki)
- **Issues:** [GitHub Issues](https://github.com/open-meteo/open-meteo/issues)

