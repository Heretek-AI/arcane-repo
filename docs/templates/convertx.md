---
title: "Convertx"
description: "Self-hosted Convertx deployment via Docker"
---

# Convertx

Self-hosted Convertx deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/convertx/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/convertx/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/convertx/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `convertx` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b4d786b97d2e0f8707a2f7d9e4ab643172fa2b1351e469e2f42c405468e48bd3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `convertx` | ghcr.io/c4illin/convertx:latest | Main application service |
| `convertx_data` | (volume) | Persistent data storage |

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
| `CONVERTX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs convertx
```

**Port conflict:**
Edit `.env` and change `CONVERTX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec convertx ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect convertx --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v convertx_data:/data -v $(pwd):/backup alpine tar czf /backup/convertx-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v convertx_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/convertx-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Convertx](https://github.com/c4illin/convertx)
- **Docker Image:** `ghcr.io/c4illin/convertx:latest`
- **Documentation:** [GitHub Wiki](https://github.com/c4illin/convertx/wiki)
- **Issues:** [GitHub Issues](https://github.com/c4illin/convertx/issues)

