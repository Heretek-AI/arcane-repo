---
title: "Ghostfolio"
description: "Self-hosted Ghostfolio deployment via Docker"
---

# Ghostfolio

Self-hosted Ghostfolio deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ghostfolio/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ghostfolio/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ghostfolio/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ghostfolio` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `552e3b4d664737e0e9e13140a7cef600a42c10fc458b347e3b80454e5cdea4d0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ghostfolio` | docker.io/ghostfolio/ghostfolio:latest | Main application service |
| `ghostfolio_data` | (volume) | Persistent data storage |

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
| `GHOSTFOLIO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs ghostfolio
```

**Port conflict:**
Edit `.env` and change `GHOSTFOLIO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ghostfolio ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ghostfolio --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ghostfolio_data:/data -v $(pwd):/backup alpine tar czf /backup/ghostfolio-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ghostfolio_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ghostfolio-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Ghostfolio](https://github.com/ghostfolio/ghostfolio)
- **Docker Image:** `docker.io/ghostfolio/ghostfolio:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ghostfolio/ghostfolio/wiki)
- **Issues:** [GitHub Issues](https://github.com/ghostfolio/ghostfolio/issues)

