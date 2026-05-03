---
title: "Linkace"
description: "Self-hosted Linkace deployment via Docker"
---

# Linkace

Self-hosted Linkace deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkace/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkace/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/linkace/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `linkace` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b24b32bc89364b437bc91facd24651c946cffde1afc40765e1e743c9262b1c6c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `linkace` | docker.io/linkace/linkace:latest | Main application service |
| `linkace_data` | (volume) | Persistent data storage |

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
| `LINKACE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs linkace
```

**Port conflict:**
Edit `.env` and change `LINKACE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec linkace ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect linkace --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v linkace_data:/data -v $(pwd):/backup alpine tar czf /backup/linkace-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v linkace_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/linkace-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Linkace](https://github.com/linkace/linkace)
- **Docker Image:** `docker.io/linkace/linkace:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linkace/linkace/wiki)
- **Issues:** [GitHub Issues](https://github.com/linkace/linkace/issues)

