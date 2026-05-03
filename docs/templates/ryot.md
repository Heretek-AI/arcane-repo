---
title: "Ryot"
description: "Self-hosted Ryot deployment via Docker"
---

# Ryot

Self-hosted Ryot deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ryot/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ryot/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ryot/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ryot` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `535517cd3173b5259b505da064b185b50461ddebef33ded8d508e479a3bbab0b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ryot` | ghcr.io/ignisda/ryot:latest | Main application service |
| `ryot_data` | (volume) | Persistent data storage |

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
| `RYOT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs ryot
```

**Port conflict:**
Edit `.env` and change `RYOT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ryot ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ryot --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ryot_data:/data -v $(pwd):/backup alpine tar czf /backup/ryot-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ryot_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ryot-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Ryot](https://github.com/ignisda/ryot)
- **Docker Image:** `ghcr.io/ignisda/ryot:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ignisda/ryot/wiki)
- **Issues:** [GitHub Issues](https://github.com/ignisda/ryot/issues)

