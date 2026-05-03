---
title: "Yamtrack"
description: "Self-hosted Yamtrack deployment via Docker"
---

# Yamtrack

Self-hosted Yamtrack deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yamtrack/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yamtrack/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yamtrack/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `yamtrack` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `57e6dbf02df65ad11bfa03aeefb853b1910951ee72792aaafda3accd5087f893` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `yamtrack` | docker.io/dmintz37/yamtrack:latest | Main application service |
| `yamtrack_data` | (volume) | Persistent data storage |

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
| `YAMTRACK_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs yamtrack
```

**Port conflict:**
Edit `.env` and change `YAMTRACK_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec yamtrack ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect yamtrack --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v yamtrack_data:/data -v $(pwd):/backup alpine tar czf /backup/yamtrack-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v yamtrack_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/yamtrack-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Yamtrack](https://github.com/dmintz37/yamtrack)
- **Docker Image:** `docker.io/dmintz37/yamtrack:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dmintz37/yamtrack/wiki)
- **Issues:** [GitHub Issues](https://github.com/dmintz37/yamtrack/issues)

