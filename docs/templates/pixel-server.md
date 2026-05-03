---
title: "Pixel Server"
description: "Self-hosted Pixel Server deployment via Docker"
---

# Pixel Server

Self-hosted Pixel Server deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pixel-server/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pixel-server/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pixel-server/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pixel-server` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3a269f5eeb10513b3c2ea3c80ebaf83b86109b513cb127e43da1cc3bedcb71aa` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pixel-server` | docker.io/olegvorobyov90/pixel-server:latest | Main application service |
| `pixel-server_data` | (volume) | Persistent data storage |

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
| `PIXEL_SERVER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pixel-server
```

**Port conflict:**
Edit `.env` and change `PIXEL-SERVER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pixel-server ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pixel-server --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pixel-server_data:/data -v $(pwd):/backup alpine tar czf /backup/pixel-server-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pixel-server_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pixel-server-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pixel Server](https://github.com/olegvorobyov90/pixel-server)
- **Docker Image:** `docker.io/olegvorobyov90/pixel-server:latest`
- **Documentation:** [GitHub Wiki](https://github.com/olegvorobyov90/pixel-server/wiki)
- **Issues:** [GitHub Issues](https://github.com/olegvorobyov90/pixel-server/issues)

