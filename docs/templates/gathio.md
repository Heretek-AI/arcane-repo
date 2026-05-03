---
title: "Gathio"
description: "Self-hosted Gathio deployment via Docker"
---

# Gathio

Self-hosted Gathio deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gathio/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gathio/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gathio/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gathio` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `445b3e85cc05f39d26e54e3e8fbb5f8da9455ec80f5e64ea99e4c22f35c67225` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gathio` | docker.io/pheezer/gathio:latest | Main application service |
| `gathio_data` | (volume) | Persistent data storage |

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
| `GATHIO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gathio
```

**Port conflict:**
Edit `.env` and change `GATHIO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gathio ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gathio --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gathio_data:/data -v $(pwd):/backup alpine tar czf /backup/gathio-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gathio_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gathio-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gathio](https://github.com/pheezer/gathio)
- **Docker Image:** `docker.io/pheezer/gathio:latest`
- **Documentation:** [GitHub Wiki](https://github.com/pheezer/gathio/wiki)
- **Issues:** [GitHub Issues](https://github.com/pheezer/gathio/issues)

