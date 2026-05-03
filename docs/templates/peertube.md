---
title: "Peertube"
description: "Self-hosted Peertube deployment via Docker"
---

# Peertube

Self-hosted Peertube deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/peertube/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/peertube/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/peertube/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `peertube` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `33385a30addbade61c6fff737ed4909f3deeaf439276aeb2ec9151f02030b27a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `peertube` | docker.io/chocobozzz/peertube:latest | Main application service |
| `peertube_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:9000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9000](http://localhost:9000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `PEERTUBE_PORT` | `9000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs peertube
```

**Port conflict:**
Edit `.env` and change `PEERTUBE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec peertube ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect peertube --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v peertube_data:/data -v $(pwd):/backup alpine tar czf /backup/peertube-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v peertube_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/peertube-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Peertube](https://github.com/chocobozzz/peertube)
- **Docker Image:** `docker.io/chocobozzz/peertube:latest`
- **Documentation:** [GitHub Wiki](https://github.com/chocobozzz/peertube/wiki)
- **Issues:** [GitHub Issues](https://github.com/chocobozzz/peertube/issues)

