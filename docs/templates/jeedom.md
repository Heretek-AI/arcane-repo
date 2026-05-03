---
title: "Jeedom"
description: "Self-hosted Jeedom deployment via Docker"
---

# Jeedom

Self-hosted Jeedom deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jeedom/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jeedom/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jeedom/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `jeedom` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5cd6f06bda9b6a3e63c859ff3578314a2a6777d61e8b57f17070232e8bd4664b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `jeedom` | docker.io/jeedom/jeedom:latest | Main application service |
| `jeedom_data` | (volume) | Persistent data storage |

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
| `JEEDOM_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs jeedom
```

**Port conflict:**
Edit `.env` and change `JEEDOM_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec jeedom ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect jeedom --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v jeedom_data:/data -v $(pwd):/backup alpine tar czf /backup/jeedom-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v jeedom_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/jeedom-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Jeedom](https://github.com/jeedom/jeedom)
- **Docker Image:** `docker.io/jeedom/jeedom:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jeedom/jeedom/wiki)
- **Issues:** [GitHub Issues](https://github.com/jeedom/jeedom/issues)

