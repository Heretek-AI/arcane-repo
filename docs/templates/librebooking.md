---
title: "Librebooking"
description: "Self-hosted Librebooking deployment via Docker"
---

# Librebooking

Self-hosted Librebooking deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/librebooking/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/librebooking/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/librebooking/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `librebooking` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b8e8c79af095f9fa0f1475de823956e6e090ad69bf6d8470d59f4007fb65f3e3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `librebooking` | docker.io/librebooking/librebooking:latest | Main application service |
| `librebooking_data` | (volume) | Persistent data storage |

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
| `LIBREBOOKING_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs librebooking
```

**Port conflict:**
Edit `.env` and change `LIBREBOOKING_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec librebooking ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect librebooking --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v librebooking_data:/data -v $(pwd):/backup alpine tar czf /backup/librebooking-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v librebooking_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/librebooking-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Librebooking](https://github.com/librebooking/librebooking)
- **Docker Image:** `docker.io/librebooking/librebooking:latest`
- **Documentation:** [GitHub Wiki](https://github.com/librebooking/librebooking/wiki)
- **Issues:** [GitHub Issues](https://github.com/librebooking/librebooking/issues)

