---
title: "Gitea"
description: "Self-hosted Gitea deployment via Docker"
---

# Gitea

Self-hosted Gitea deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gitea/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gitea/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gitea/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gitea` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `bcbc6811d2352368ffda32508f30bc1014581638f3e8d7ce61cfcef43b736b02` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gitea` | docker.io/gitea/gitea:latest | Main application service |
| `gitea_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:3000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `GITEA_PORT` | `3000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gitea
```

**Port conflict:**
Edit `.env` and change `GITEA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gitea ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gitea --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gitea_data:/data -v $(pwd):/backup alpine tar czf /backup/gitea-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gitea_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gitea-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gitea](https://github.com/gitea/gitea)
- **Docker Image:** `docker.io/gitea/gitea:latest`
- **Documentation:** [GitHub Wiki](https://github.com/gitea/gitea/wiki)
- **Issues:** [GitHub Issues](https://github.com/gitea/gitea/issues)

