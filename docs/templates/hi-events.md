---
title: "Hi.Events"
description: "Self-hosted Hi.Events deployment via Docker"
---

# Hi.Events

Self-hosted Hi.Events deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hi-events/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hi-events/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hi-events/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `hi-events` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `db0713263a4da277716424d9d5154a40f219d5ddb459caa156863c556a559426` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `hi-events` | docker.io/dciangot/hi.events:latest | Main application service |
| `hi-events_data` | (volume) | Persistent data storage |

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
| `HI_EVENTS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs hi-events
```

**Port conflict:**
Edit `.env` and change `HI-EVENTS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec hi-events ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect hi-events --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v hi-events_data:/data -v $(pwd):/backup alpine tar czf /backup/hi-events-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v hi-events_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/hi-events-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Hi.Events](https://github.com/dciangot/hi.events)
- **Docker Image:** `docker.io/dciangot/hi.events:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dciangot/hi.events/wiki)
- **Issues:** [GitHub Issues](https://github.com/dciangot/hi.events/issues)

