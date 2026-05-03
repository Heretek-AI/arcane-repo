---
title: "Dittofeed"
description: "Self-hosted Dittofeed deployment via Docker"
---

# Dittofeed

Self-hosted Dittofeed deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dittofeed/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dittofeed/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dittofeed/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dittofeed` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `70c955a3f4b28c87a1ea2baf6cee4c1581354749523d93f0733cbaae109aff26` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dittofeed` | docker.io/sefiroed/dittofeed:latest | Main application service |
| `dittofeed_data` | (volume) | Persistent data storage |

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
| `DITTOFEED_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dittofeed
```

**Port conflict:**
Edit `.env` and change `DITTOFEED_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dittofeed ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dittofeed --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dittofeed_data:/data -v $(pwd):/backup alpine tar czf /backup/dittofeed-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dittofeed_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dittofeed-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dittofeed](https://github.com/sefiroed/dittofeed)
- **Docker Image:** `docker.io/sefiroed/dittofeed:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sefiroed/dittofeed/wiki)
- **Issues:** [GitHub Issues](https://github.com/sefiroed/dittofeed/issues)

