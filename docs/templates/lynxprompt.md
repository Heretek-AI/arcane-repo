---
title: "Lynxprompt"
description: "Self-hosted Lynxprompt deployment via Docker"
---

# Lynxprompt

Self-hosted Lynxprompt deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lynxprompt/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lynxprompt/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lynxprompt/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `lynxprompt` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `a27bea4b2d9da836800f41c6605ac2a4f4878fd8134d021d595212ca07b49d2f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `lynxprompt` | docker.io/drumsergio/lynxprompt:latest | Main application service |
| `lynxprompt_data` | (volume) | Persistent data storage |

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
| `LYNXPROMPT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs lynxprompt
```

**Port conflict:**
Edit `.env` and change `LYNXPROMPT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec lynxprompt ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect lynxprompt --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v lynxprompt_data:/data -v $(pwd):/backup alpine tar czf /backup/lynxprompt-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v lynxprompt_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/lynxprompt-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Lynxprompt](https://github.com/drumsergio/lynxprompt)
- **Docker Image:** `docker.io/drumsergio/lynxprompt:latest`
- **Documentation:** [GitHub Wiki](https://github.com/drumsergio/lynxprompt/wiki)
- **Issues:** [GitHub Issues](https://github.com/drumsergio/lynxprompt/issues)

