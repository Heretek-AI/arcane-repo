---
title: "Pangolin"
description: "Self-hosted Pangolin deployment via Docker"
---

# Pangolin

Self-hosted Pangolin deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pangolin/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pangolin/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pangolin/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pangolin` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `516435e1f7fad4d03cf7a174d8dc079e39fb32e7a3c28fec3b568b52b5b5aade` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pangolin` | docker.io/staphb/pangolin:latest | Main application service |
| `pangolin_data` | (volume) | Persistent data storage |

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
| `PANGOLIN_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pangolin
```

**Port conflict:**
Edit `.env` and change `PANGOLIN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pangolin ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pangolin --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pangolin_data:/data -v $(pwd):/backup alpine tar czf /backup/pangolin-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pangolin_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pangolin-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pangolin](https://github.com/staphb/pangolin)
- **Docker Image:** `docker.io/staphb/pangolin:latest`
- **Documentation:** [GitHub Wiki](https://github.com/staphb/pangolin/wiki)
- **Issues:** [GitHub Issues](https://github.com/staphb/pangolin/issues)

