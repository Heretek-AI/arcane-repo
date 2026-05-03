---
title: "Bookstack"
description: "Self-hosted Bookstack deployment via Docker"
---

# Bookstack

Self-hosted Bookstack deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bookstack/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bookstack/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bookstack/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bookstack` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d1bfbe0effad0ef78e182a5d9d77ab0d00151f05566bc689c31e091018a99b46` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `bookstack` | ghcr.io/linuxserver/bookstack:latest | Main application service |
| `bookstack_data` | (volume) | Persistent data storage |

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
| `BOOKSTACK_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs bookstack
```

**Port conflict:**
Edit `.env` and change `BOOKSTACK_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec bookstack ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect bookstack --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v bookstack_data:/data -v $(pwd):/backup alpine tar czf /backup/bookstack-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v bookstack_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/bookstack-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Bookstack](https://github.com/linuxserver/bookstack)
- **Docker Image:** `ghcr.io/linuxserver/bookstack:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/bookstack/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/bookstack/issues)

