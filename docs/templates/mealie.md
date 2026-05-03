---
title: "Mealie"
description: "Self-hosted Mealie deployment via Docker"
---

# Mealie

Self-hosted Mealie deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mealie/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mealie/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mealie/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mealie` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ebfc45b87314ccbec5a211686ce54505fcbeb6bd390431e0e84cb4051e0e290a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mealie` | docker.io/hkotel/mealie:latest | Main application service |
| `mealie_data` | (volume) | Persistent data storage |

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
| `MEALIE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mealie
```

**Port conflict:**
Edit `.env` and change `MEALIE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mealie ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mealie --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mealie_data:/data -v $(pwd):/backup alpine tar czf /backup/mealie-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mealie_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mealie-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mealie](https://github.com/hkotel/mealie)
- **Docker Image:** `docker.io/hkotel/mealie:latest`
- **Documentation:** [GitHub Wiki](https://github.com/hkotel/mealie/wiki)
- **Issues:** [GitHub Issues](https://github.com/hkotel/mealie/issues)

