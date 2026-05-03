---
title: "Codex"
description: "Self-hosted Codex deployment via Docker"
---

# Codex

Self-hosted Codex deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/codex/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/codex/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/codex/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `codex` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ee83671464dc0c892eeb481296c17ef704052cfd757a83ac1d8e5780ed3fa454` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `codex` | ghcr.io/ajslater/codex:latest | Main application service |
| `codex_data` | (volume) | Persistent data storage |

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
| `CODEX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs codex
```

**Port conflict:**
Edit `.env` and change `CODEX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec codex ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect codex --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v codex_data:/data -v $(pwd):/backup alpine tar czf /backup/codex-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v codex_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/codex-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Codex](https://github.com/ajslater/codex)
- **Docker Image:** `ghcr.io/ajslater/codex:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ajslater/codex/wiki)
- **Issues:** [GitHub Issues](https://github.com/ajslater/codex/issues)

