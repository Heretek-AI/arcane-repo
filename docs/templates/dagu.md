---
title: "Dagu"
description: "Self-hosted Dagu deployment via Docker"
---

# Dagu

Self-hosted Dagu deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dagu/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dagu/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dagu/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dagu` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `75313d9373c17de18335898ddba2ccc3d3f84089fb80abb260835d63ebd068e1` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dagu` | docker.io/coralhl/dagu:latest | Main application service |
| `dagu_data` | (volume) | Persistent data storage |

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
| `DAGU_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dagu
```

**Port conflict:**
Edit `.env` and change `DAGU_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dagu ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dagu --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dagu_data:/data -v $(pwd):/backup alpine tar czf /backup/dagu-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dagu_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dagu-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dagu](https://github.com/coralhl/dagu)
- **Docker Image:** `docker.io/coralhl/dagu:latest`
- **Documentation:** [GitHub Wiki](https://github.com/coralhl/dagu/wiki)
- **Issues:** [GitHub Issues](https://github.com/coralhl/dagu/issues)

