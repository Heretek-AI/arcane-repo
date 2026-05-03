---
title: "Viseron"
description: "Self-hosted Viseron deployment via Docker"
---

# Viseron

Self-hosted Viseron deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/viseron/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/viseron/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/viseron/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `viseron` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `14413ea087e348c7831c5d6559b549f29b60c1ba3ed03e393436571cb4b37433` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `viseron` | docker.io/roflcoopter/viseron:latest | Main application service |
| `viseron_data` | (volume) | Persistent data storage |

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
| `VISERON_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs viseron
```

**Port conflict:**
Edit `.env` and change `VISERON_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec viseron ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect viseron --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v viseron_data:/data -v $(pwd):/backup alpine tar czf /backup/viseron-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v viseron_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/viseron-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Viseron](https://github.com/roflcoopter/viseron)
- **Docker Image:** `docker.io/roflcoopter/viseron:latest`
- **Documentation:** [GitHub Wiki](https://github.com/roflcoopter/viseron/wiki)
- **Issues:** [GitHub Issues](https://github.com/roflcoopter/viseron/issues)

