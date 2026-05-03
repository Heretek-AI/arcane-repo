---
title: "Syncthing"
description: "Self-hosted Syncthing deployment via Docker"
---

# Syncthing

Self-hosted Syncthing deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/storage" class="tag-badge">storage</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/syncthing/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/syncthing/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/syncthing/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `syncthing` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b49896a3d532c78084e501e06a232e8f835e8f8f9bf567c42f913163f351c044` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `syncthing` | ghcr.io/syncthing/syncthing:latest | Main application service |
| `syncthing_data` | (volume) | Persistent data storage |

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
| `SYNCTHING_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs syncthing
```

**Port conflict:**
Edit `.env` and change `SYNCTHING_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec syncthing ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect syncthing --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v syncthing_data:/data -v $(pwd):/backup alpine tar czf /backup/syncthing-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v syncthing_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/syncthing-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Syncthing](https://github.com/syncthing/syncthing)
- **Docker Image:** `ghcr.io/syncthing/syncthing:latest`
- **Documentation:** [GitHub Wiki](https://github.com/syncthing/syncthing/wiki)
- **Issues:** [GitHub Issues](https://github.com/syncthing/syncthing/issues)

