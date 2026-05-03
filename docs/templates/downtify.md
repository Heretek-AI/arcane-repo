---
title: "Downtify"
description: "Self-hosted Downtify deployment via Docker"
---

# Downtify

Self-hosted Downtify deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/downtify/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/downtify/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/downtify/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `downtify` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b60794c22be8eac5a27e8d4101c1f5c308cd32251b9c63e386318088c206ca9f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `downtify` | ghcr.io/henriquesebastiao/downtify:latest | Main application service |
| `downtify_data` | (volume) | Persistent data storage |

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
| `DOWNTIFY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs downtify
```

**Port conflict:**
Edit `.env` and change `DOWNTIFY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec downtify ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect downtify --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v downtify_data:/data -v $(pwd):/backup alpine tar czf /backup/downtify-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v downtify_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/downtify-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Downtify](https://github.com/henriquesebastiao/downtify)
- **Docker Image:** `ghcr.io/henriquesebastiao/downtify:latest`
- **Documentation:** [GitHub Wiki](https://github.com/henriquesebastiao/downtify/wiki)
- **Issues:** [GitHub Issues](https://github.com/henriquesebastiao/downtify/issues)

