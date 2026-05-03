---
title: "Shaarli"
description: "Self-hosted Shaarli deployment via Docker"
---

# Shaarli

Self-hosted Shaarli deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shaarli/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shaarli/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shaarli/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `shaarli` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4f69feb245e5176f15de59edf94dc7c7376a5a2e20b9fa94152f68d6fb53b9f8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `shaarli` | ghcr.io/shaarli/shaarli:latest | Main application service |
| `shaarli_data` | (volume) | Persistent data storage |

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
| `SHAARLI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs shaarli
```

**Port conflict:**
Edit `.env` and change `SHAARLI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec shaarli ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect shaarli --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v shaarli_data:/data -v $(pwd):/backup alpine tar czf /backup/shaarli-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v shaarli_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/shaarli-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Shaarli](https://github.com/shaarli/shaarli)
- **Docker Image:** `ghcr.io/shaarli/shaarli:latest`
- **Documentation:** [GitHub Wiki](https://github.com/shaarli/shaarli/wiki)
- **Issues:** [GitHub Issues](https://github.com/shaarli/shaarli/issues)

