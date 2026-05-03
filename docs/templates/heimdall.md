---
title: "Heimdall"
description: "Self-hosted Heimdall deployment via Docker"
---

# Heimdall

Self-hosted Heimdall deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/heimdall/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/heimdall/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/heimdall/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `heimdall` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b2d2ed6ab305c3cb1078a9b9cbf763106d3a02c5d5558f43d0d7db4e3dfcd0d3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `heimdall` | ghcr.io/linuxserver/heimdall:latest | Main application service |
| `heimdall_data` | (volume) | Persistent data storage |

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
| `HEIMDALL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs heimdall
```

**Port conflict:**
Edit `.env` and change `HEIMDALL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec heimdall ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect heimdall --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v heimdall_data:/data -v $(pwd):/backup alpine tar czf /backup/heimdall-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v heimdall_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/heimdall-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Heimdall](https://github.com/linuxserver/heimdall)
- **Docker Image:** `ghcr.io/linuxserver/heimdall:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/heimdall/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/heimdall/issues)

