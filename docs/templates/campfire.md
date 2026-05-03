---
title: "Campfire"
description: "Self-hosted Campfire deployment via Docker"
---

# Campfire

Self-hosted Campfire deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/campfire/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/campfire/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/campfire/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `campfire` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `eac8bb74411c6d82363abaf08bb909a35e48cbec6c9d4a16684210ee45f3661a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `campfire` | docker.io/xw134/campfire:latest | Main application service |
| `campfire_data` | (volume) | Persistent data storage |

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
| `CAMPFIRE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs campfire
```

**Port conflict:**
Edit `.env` and change `CAMPFIRE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec campfire ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect campfire --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v campfire_data:/data -v $(pwd):/backup alpine tar czf /backup/campfire-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v campfire_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/campfire-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Campfire](https://github.com/xw134/campfire)
- **Docker Image:** `docker.io/xw134/campfire:latest`
- **Documentation:** [GitHub Wiki](https://github.com/xw134/campfire/wiki)
- **Issues:** [GitHub Issues](https://github.com/xw134/campfire/issues)

