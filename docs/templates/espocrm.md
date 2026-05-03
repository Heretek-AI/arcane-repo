---
title: "Espocrm"
description: "Self-hosted Espocrm deployment via Docker"
---

# Espocrm

Self-hosted Espocrm deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/espocrm/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/espocrm/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/espocrm/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `espocrm` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c675640cff7a2d38ac11090982ac1df593f0d73c9751bc908c1a3f8eb896e2ee` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `espocrm` | docker.io/espocrm/espocrm:latest | Main application service |
| `espocrm_data` | (volume) | Persistent data storage |

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
| `ESPOCRM_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs espocrm
```

**Port conflict:**
Edit `.env` and change `ESPOCRM_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec espocrm ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect espocrm --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v espocrm_data:/data -v $(pwd):/backup alpine tar czf /backup/espocrm-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v espocrm_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/espocrm-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Espocrm](https://github.com/espocrm/espocrm)
- **Docker Image:** `docker.io/espocrm/espocrm:latest`
- **Documentation:** [GitHub Wiki](https://github.com/espocrm/espocrm/wiki)
- **Issues:** [GitHub Issues](https://github.com/espocrm/espocrm/issues)

