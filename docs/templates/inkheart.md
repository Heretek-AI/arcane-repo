---
title: "Inkheart"
description: "Self-hosted Inkheart deployment via Docker"
---

# Inkheart

Self-hosted Inkheart deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/inkheart/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/inkheart/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/inkheart/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `inkheart` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a6bd8e21430ffaa72721386e0c68fc833f115dedd4471fd109f27c3ba57e358f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `inkheart` | docker.io/nobbe/inkheart:latest | Main application service |
| `inkheart_data` | (volume) | Persistent data storage |

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
| `INKHEART_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs inkheart
```

**Port conflict:**
Edit `.env` and change `INKHEART_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec inkheart ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect inkheart --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v inkheart_data:/data -v $(pwd):/backup alpine tar czf /backup/inkheart-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v inkheart_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/inkheart-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Inkheart](https://github.com/nobbe/inkheart)
- **Docker Image:** `docker.io/nobbe/inkheart:latest`
- **Documentation:** [GitHub Wiki](https://github.com/nobbe/inkheart/wiki)
- **Issues:** [GitHub Issues](https://github.com/nobbe/inkheart/issues)

