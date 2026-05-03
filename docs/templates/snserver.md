---
title: "Snserver"
description: "Self-hosted Snserver deployment via Docker"
---

# Snserver

Self-hosted Snserver deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/snserver/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/snserver/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/snserver/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `snserver` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `be89b9de4a1820ed9ca9253c1d062d8df82f3d6161e4aa0da5d3ca7f49a51c3d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `snserver` | docker.io/isamaya/snserver:latest | Main application service |
| `snserver_data` | (volume) | Persistent data storage |

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
| `SNSERVER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs snserver
```

**Port conflict:**
Edit `.env` and change `SNSERVER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec snserver ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect snserver --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v snserver_data:/data -v $(pwd):/backup alpine tar czf /backup/snserver-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v snserver_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/snserver-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Snserver](https://github.com/isamaya/snserver)
- **Docker Image:** `docker.io/isamaya/snserver:latest`
- **Documentation:** [GitHub Wiki](https://github.com/isamaya/snserver/wiki)
- **Issues:** [GitHub Issues](https://github.com/isamaya/snserver/issues)

