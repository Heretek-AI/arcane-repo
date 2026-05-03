---
title: "Castopod"
description: "Self-hosted Castopod deployment via Docker"
---

# Castopod

Self-hosted Castopod deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/castopod/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/castopod/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/castopod/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `castopod` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `96b9519a26e33d67f86c8051b388b773189a121599b6323671d7aba3764f99f3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `castopod` | docker.io/castopod/castopod:latest | Main application service |
| `castopod_data` | (volume) | Persistent data storage |

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
| `CASTOPOD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs castopod
```

**Port conflict:**
Edit `.env` and change `CASTOPOD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec castopod ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect castopod --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v castopod_data:/data -v $(pwd):/backup alpine tar czf /backup/castopod-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v castopod_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/castopod-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Castopod](https://github.com/castopod/castopod)
- **Docker Image:** `docker.io/castopod/castopod:latest`
- **Documentation:** [GitHub Wiki](https://github.com/castopod/castopod/wiki)
- **Issues:** [GitHub Issues](https://github.com/castopod/castopod/issues)

