---
title: "Discourse"
description: "Self-hosted Discourse deployment via Docker"
---

# Discourse

Self-hosted Discourse deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/discourse/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/discourse/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/discourse/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `discourse` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `968b2d2cd3e0db9011c3e11a8041d49bb4afa11d00306d6ffcddaa708e5209ee` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `discourse` | docker.io/discourse/discourse:latest | Main application service |
| `discourse_data` | (volume) | Persistent data storage |

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
| `DISCOURSE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs discourse
```

**Port conflict:**
Edit `.env` and change `DISCOURSE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec discourse ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect discourse --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v discourse_data:/data -v $(pwd):/backup alpine tar czf /backup/discourse-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v discourse_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/discourse-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Discourse](https://github.com/discourse/discourse)
- **Docker Image:** `docker.io/discourse/discourse:latest`
- **Documentation:** [GitHub Wiki](https://github.com/discourse/discourse/wiki)
- **Issues:** [GitHub Issues](https://github.com/discourse/discourse/issues)

