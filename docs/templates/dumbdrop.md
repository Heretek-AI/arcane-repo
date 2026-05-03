---
title: "Dumbdrop"
description: "Self-hosted Dumbdrop deployment via Docker"
---

# Dumbdrop

Self-hosted Dumbdrop deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbdrop/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbdrop/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbdrop/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dumbdrop` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `33a4ae0da65832c7d82f6cbc3e7c29f24f8495c04e4bbd8d2583c1a0c6755d87` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dumbdrop` | docker.io/dumbwareio/dumbdrop:latest | Main application service |
| `dumbdrop_data` | (volume) | Persistent data storage |

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
| `DUMBDROP_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dumbdrop
```

**Port conflict:**
Edit `.env` and change `DUMBDROP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dumbdrop ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dumbdrop --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dumbdrop_data:/data -v $(pwd):/backup alpine tar czf /backup/dumbdrop-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dumbdrop_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dumbdrop-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dumbdrop](https://github.com/dumbwareio/dumbdrop)
- **Docker Image:** `docker.io/dumbwareio/dumbdrop:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dumbwareio/dumbdrop/wiki)
- **Issues:** [GitHub Issues](https://github.com/dumbwareio/dumbdrop/issues)

