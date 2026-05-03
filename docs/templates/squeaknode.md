---
title: "Squeaknode"
description: "Self-hosted Squeaknode deployment via Docker"
---

# Squeaknode

Self-hosted Squeaknode deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/squeaknode/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/squeaknode/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/squeaknode/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `squeaknode` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `0a29048599b0d40da161f9a7e74a7616de4c5ad079ff693c48aae081bbe05f27` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `squeaknode` | ghcr.io/squeaknode/squeaknode:latest | Main application service |
| `squeaknode_data` | (volume) | Persistent data storage |

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
| `SQUEAKNODE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs squeaknode
```

**Port conflict:**
Edit `.env` and change `SQUEAKNODE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec squeaknode ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect squeaknode --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v squeaknode_data:/data -v $(pwd):/backup alpine tar czf /backup/squeaknode-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v squeaknode_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/squeaknode-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Squeaknode](https://github.com/squeaknode/squeaknode)
- **Docker Image:** `ghcr.io/squeaknode/squeaknode:latest`
- **Documentation:** [GitHub Wiki](https://github.com/squeaknode/squeaknode/wiki)
- **Issues:** [GitHub Issues](https://github.com/squeaknode/squeaknode/issues)

