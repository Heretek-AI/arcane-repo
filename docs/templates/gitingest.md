---
title: "Gitingest"
description: "Self-hosted Gitingest deployment via Docker"
---

# Gitingest

Self-hosted Gitingest deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gitingest/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gitingest/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gitingest/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gitingest` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c2ce79e58fbac0554b692b5723af1caa59d8257831c1118ff41cc454924fd125` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gitingest` | docker.io/elestio/gitingest:latest | Main application service |
| `gitingest_data` | (volume) | Persistent data storage |

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
| `GITINGEST_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gitingest
```

**Port conflict:**
Edit `.env` and change `GITINGEST_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gitingest ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gitingest --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gitingest_data:/data -v $(pwd):/backup alpine tar czf /backup/gitingest-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gitingest_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gitingest-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gitingest](https://github.com/elestio/gitingest)
- **Docker Image:** `docker.io/elestio/gitingest:latest`
- **Documentation:** [GitHub Wiki](https://github.com/elestio/gitingest/wiki)
- **Issues:** [GitHub Issues](https://github.com/elestio/gitingest/issues)

