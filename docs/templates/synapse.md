---
title: "Synapse"
description: "Self-hosted Synapse deployment via Docker"
---

# Synapse

Self-hosted Synapse deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/synapse/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/synapse/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/synapse/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `synapse` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f75a1f610da4fc84e51ac6b206c3addd4a09ef42dc386e42eae7fc44915fb5a0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `synapse` | docker.io/matrixdotorg/synapse:latest | Main application service |
| `synapse_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8008/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8008](http://localhost:8008) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNAPSE_PORT` | `8008` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs synapse
```

**Port conflict:**
Edit `.env` and change `SYNAPSE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec synapse ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect synapse --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v synapse_data:/data -v $(pwd):/backup alpine tar czf /backup/synapse-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v synapse_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/synapse-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Synapse](https://github.com/matrixdotorg/synapse)
- **Docker Image:** `docker.io/matrixdotorg/synapse:latest`
- **Documentation:** [GitHub Wiki](https://github.com/matrixdotorg/synapse/wiki)
- **Issues:** [GitHub Issues](https://github.com/matrixdotorg/synapse/issues)

