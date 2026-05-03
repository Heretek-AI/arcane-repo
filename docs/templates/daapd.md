---
title: "Daapd"
description: "Self-hosted Daapd deployment via Docker"
---

# Daapd

Self-hosted Daapd deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/daapd/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/daapd/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/daapd/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `daapd` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a9fd0fa9bf347c94fdc21ae0ae4da8ffc929df5586413d573057aafa06481111` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `daapd` | ghcr.io/linuxserver/daapd:latest | Main application service |
| `daapd_data` | (volume) | Persistent data storage |

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
| `DAAPD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs daapd
```

**Port conflict:**
Edit `.env` and change `DAAPD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec daapd ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect daapd --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v daapd_data:/data -v $(pwd):/backup alpine tar czf /backup/daapd-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v daapd_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/daapd-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Daapd](https://github.com/linuxserver/daapd)
- **Docker Image:** `ghcr.io/linuxserver/daapd:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/daapd/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/daapd/issues)

