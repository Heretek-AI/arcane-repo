---
title: "Pihole"
description: "Self-hosted Pihole deployment via Docker"
---

# Pihole

Self-hosted Pihole deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pihole/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pihole/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pihole/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pihole` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `69339eea1cc7ca0e5a4e7dbb3537039cf3a307242c9d02a3ffd969827aefc434` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pihole` | docker.io/pihole/pihole:latest | Main application service |
| `pihole_data` | (volume) | Persistent data storage |

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
| `PIHOLE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pihole
```

**Port conflict:**
Edit `.env` and change `PIHOLE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pihole ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pihole --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pihole_data:/data -v $(pwd):/backup alpine tar czf /backup/pihole-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pihole_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pihole-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pihole](https://github.com/pihole/pihole)
- **Docker Image:** `docker.io/pihole/pihole:latest`
- **Documentation:** [GitHub Wiki](https://github.com/pihole/pihole/wiki)
- **Issues:** [GitHub Issues](https://github.com/pihole/pihole/issues)

