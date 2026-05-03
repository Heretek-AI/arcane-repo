---
title: "Affine"
description: "Open-source knowledge base and document workspace with real-time collaboration, whiteboards, and markdown support"
---

# Affine

Open-source knowledge base and document workspace with real-time collaboration, whiteboards, and markdown support

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/affine/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/affine/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/affine/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `affine` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3345915e142ee9c45ea47c2fb317d8a4da1f0f441295865a69002b1daf8db9c0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `affine` | docker.io/affinefoundation/affine:latest | Main application service |
| `affine_data` | (volume) | Persistent data storage |

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
| `AFFINE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs affine
```

**Port conflict:**
Edit `.env` and change `AFFINE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec affine ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect affine --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v affine_data:/data -v $(pwd):/backup alpine tar czf /backup/affine-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v affine_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/affine-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Affine](https://github.com/affinefoundation/affine)
- **Docker Image:** `docker.io/affinefoundation/affine:latest`
- **Documentation:** [GitHub Wiki](https://github.com/affinefoundation/affine/wiki)
- **Issues:** [GitHub Issues](https://github.com/affinefoundation/affine/issues)

