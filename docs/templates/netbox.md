---
title: "Netbox"
description: "Self-hosted Netbox deployment via Docker"
---

# Netbox

Self-hosted Netbox deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netbox/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netbox/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netbox/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `netbox` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b17c4b5f7fcd86267fc844966119ef82ee7822d6ed57915c63bc671660a8e6a2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `netbox` | docker.io/netboxcommunity/netbox:latest | Main application service |
| `netbox_data` | (volume) | Persistent data storage |

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
| `NETBOX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs netbox
```

**Port conflict:**
Edit `.env` and change `NETBOX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec netbox ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect netbox --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v netbox_data:/data -v $(pwd):/backup alpine tar czf /backup/netbox-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v netbox_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/netbox-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Netbox](https://github.com/netboxcommunity/netbox)
- **Docker Image:** `docker.io/netboxcommunity/netbox:latest`
- **Documentation:** [GitHub Wiki](https://github.com/netboxcommunity/netbox/wiki)
- **Issues:** [GitHub Issues](https://github.com/netboxcommunity/netbox/issues)

