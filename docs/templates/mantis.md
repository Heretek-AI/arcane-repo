---
title: "Mantis"
description: "Self-hosted Mantis deployment via Docker"
---

# Mantis

Self-hosted Mantis deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mantis/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mantis/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mantis/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mantis` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `47f45e81a999e9ac694da2e21b3b5cf3ebc5a966e7f0d212ec884f382a8108dd` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mantis` | docker.io/sublimesec/mantis:latest | Main application service |
| `mantis_data` | (volume) | Persistent data storage |

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
| `MANTIS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mantis
```

**Port conflict:**
Edit `.env` and change `MANTIS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mantis ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mantis --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mantis_data:/data -v $(pwd):/backup alpine tar czf /backup/mantis-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mantis_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mantis-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mantis](https://github.com/sublimesec/mantis)
- **Docker Image:** `docker.io/sublimesec/mantis:latest`
- **Documentation:** [GitHub Wiki](https://github.com/sublimesec/mantis/wiki)
- **Issues:** [GitHub Issues](https://github.com/sublimesec/mantis/issues)

