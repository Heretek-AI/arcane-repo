---
title: "Dumbdo"
description: "Self-hosted Dumbdo deployment via Docker"
---

# Dumbdo

Self-hosted Dumbdo deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbdo/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbdo/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbdo/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dumbdo` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d44a1bf3235b6bc31d5d54484afab2f54d42bf4788b8f8dfaaa9fc5d310eee61` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dumbdo` | docker.io/dumbwareio/dumbdo:latest | Main application service |
| `dumbdo_data` | (volume) | Persistent data storage |

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
| `DUMBDO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dumbdo
```

**Port conflict:**
Edit `.env` and change `DUMBDO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dumbdo ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dumbdo --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dumbdo_data:/data -v $(pwd):/backup alpine tar czf /backup/dumbdo-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dumbdo_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dumbdo-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dumbdo](https://github.com/dumbwareio/dumbdo)
- **Docker Image:** `docker.io/dumbwareio/dumbdo:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dumbwareio/dumbdo/wiki)
- **Issues:** [GitHub Issues](https://github.com/dumbwareio/dumbdo/issues)

