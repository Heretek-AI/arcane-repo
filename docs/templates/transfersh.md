---
title: "Transfersh"
description: "Self-hosted Transfersh deployment via Docker"
---

# Transfersh

Self-hosted Transfersh deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transfersh/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transfersh/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/transfersh/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `transfersh` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e8f542d37be2872d1b7479e4f537e4d6670ebe34032a0bc2b7312f11112b16b2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `transfersh` | docker.io/martinbouillaud/transfersh:latest | Main application service |
| `transfersh_data` | (volume) | Persistent data storage |

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
| `TRANSFERSH_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs transfersh
```

**Port conflict:**
Edit `.env` and change `TRANSFERSH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec transfersh ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect transfersh --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v transfersh_data:/data -v $(pwd):/backup alpine tar czf /backup/transfersh-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v transfersh_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/transfersh-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Transfersh](https://github.com/martinbouillaud/transfersh)
- **Docker Image:** `docker.io/martinbouillaud/transfersh:latest`
- **Documentation:** [GitHub Wiki](https://github.com/martinbouillaud/transfersh/wiki)
- **Issues:** [GitHub Issues](https://github.com/martinbouillaud/transfersh/issues)

