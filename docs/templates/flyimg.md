---
title: "Flyimg"
description: "Self-hosted Flyimg deployment via Docker"
---

# Flyimg

Self-hosted Flyimg deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flyimg/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flyimg/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flyimg/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flyimg` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7a6342a1178acf0d38c7f5871358286a64b510e5643ef9cc009a01c5dc589eca` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `flyimg` | docker.io/flyimg/flyimg:latest | Main application service |
| `flyimg_data` | (volume) | Persistent data storage |

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
| `FLYIMG_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs flyimg
```

**Port conflict:**
Edit `.env` and change `FLYIMG_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec flyimg ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect flyimg --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v flyimg_data:/data -v $(pwd):/backup alpine tar czf /backup/flyimg-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v flyimg_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/flyimg-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Flyimg](https://github.com/flyimg/flyimg)
- **Docker Image:** `docker.io/flyimg/flyimg:latest`
- **Documentation:** [GitHub Wiki](https://github.com/flyimg/flyimg/wiki)
- **Issues:** [GitHub Issues](https://github.com/flyimg/flyimg/issues)

