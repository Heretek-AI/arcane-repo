---
title: "Commandbox"
description: "Self-hosted Commandbox deployment via Docker"
---

# Commandbox

Self-hosted Commandbox deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/commandbox/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/commandbox/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/commandbox/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `commandbox` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5890292e750a96e0211d90f122979f7349a822de91c3e89842a530ea12897f45` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `commandbox` | docker.io/ortussolutions/commandbox:latest | Main application service |
| `commandbox_data` | (volume) | Persistent data storage |

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
| `COMMANDBOX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs commandbox
```

**Port conflict:**
Edit `.env` and change `COMMANDBOX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec commandbox ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect commandbox --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v commandbox_data:/data -v $(pwd):/backup alpine tar czf /backup/commandbox-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v commandbox_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/commandbox-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Commandbox](https://github.com/ortussolutions/commandbox)
- **Docker Image:** `docker.io/ortussolutions/commandbox:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ortussolutions/commandbox/wiki)
- **Issues:** [GitHub Issues](https://github.com/ortussolutions/commandbox/issues)

