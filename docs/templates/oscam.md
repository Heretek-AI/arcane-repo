---
title: "Oscam"
description: "Self-hosted Oscam deployment via Docker"
---

# Oscam

Self-hosted Oscam deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/oscam/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/oscam/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/oscam/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `oscam` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `71da29a8d2bbc39e9540f435b4e4432e213f0a2d915ceb513710792bfecf62b6` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `oscam` | ghcr.io/linuxserver/oscam:latest | Main application service |
| `oscam_data` | (volume) | Persistent data storage |

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
| `OSCAM_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs oscam
```

**Port conflict:**
Edit `.env` and change `OSCAM_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec oscam ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect oscam --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v oscam_data:/data -v $(pwd):/backup alpine tar czf /backup/oscam-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v oscam_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/oscam-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Oscam](https://github.com/linuxserver/oscam)
- **Docker Image:** `ghcr.io/linuxserver/oscam:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/oscam/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/oscam/issues)

