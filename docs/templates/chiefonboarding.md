---
title: "Chiefonboarding"
description: "Self-hosted Chiefonboarding deployment via Docker"
---

# Chiefonboarding

Self-hosted Chiefonboarding deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chiefonboarding/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chiefonboarding/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/chiefonboarding/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `chiefonboarding` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8a7125d2be13d51e6b70219c89889db065c9437d823dad0e1fc9f9ff64e9441c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `chiefonboarding` | docker.io/chiefonboarding/chiefonboarding:latest | Main application service |
| `chiefonboarding_data` | (volume) | Persistent data storage |

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
| `CHIEFONBOARDING_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs chiefonboarding
```

**Port conflict:**
Edit `.env` and change `CHIEFONBOARDING_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec chiefonboarding ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect chiefonboarding --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v chiefonboarding_data:/data -v $(pwd):/backup alpine tar czf /backup/chiefonboarding-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v chiefonboarding_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/chiefonboarding-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Chiefonboarding](https://github.com/chiefonboarding/chiefonboarding)
- **Docker Image:** `docker.io/chiefonboarding/chiefonboarding:latest`
- **Documentation:** [GitHub Wiki](https://github.com/chiefonboarding/chiefonboarding/wiki)
- **Issues:** [GitHub Issues](https://github.com/chiefonboarding/chiefonboarding/issues)

