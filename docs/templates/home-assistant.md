---
title: "Home Assistant"
description: "Self-hosted Home Assistant deployment via Docker"
---

# Home Assistant

Self-hosted Home Assistant deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/home-assistant/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/home-assistant/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/home-assistant/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `home-assistant` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f50adf7dbfc0d09d5fd4a2674f2ad9dbe25508b91174ef2ebf007e218bc38d37` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `home-assistant` | ghcr.io/home-assistant/home-assistant:latest | Main application service |
| `home-assistant_data` | (volume) | Persistent data storage |

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
| `HOME_ASSISTANT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs home-assistant
```

**Port conflict:**
Edit `.env` and change `HOME-ASSISTANT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec home-assistant ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect home-assistant --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v home-assistant_data:/data -v $(pwd):/backup alpine tar czf /backup/home-assistant-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v home-assistant_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/home-assistant-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Home Assistant](https://github.com/home-assistant/home-assistant)
- **Docker Image:** `ghcr.io/home-assistant/home-assistant:latest`
- **Documentation:** [GitHub Wiki](https://github.com/home-assistant/home-assistant/wiki)
- **Issues:** [GitHub Issues](https://github.com/home-assistant/home-assistant/issues)

