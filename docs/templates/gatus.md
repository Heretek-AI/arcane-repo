---
title: "Gatus"
description: "Self-hosted Gatus deployment via Docker"
---

# Gatus

Self-hosted Gatus deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gatus/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gatus/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gatus/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gatus` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f3be776aaa5dfe4ddb7f7c548ab00babe1ed15bf707128adc56e894de1196703` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gatus` | docker.io/twinproduction/gatus:latest | Main application service |
| `gatus_data` | (volume) | Persistent data storage |

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
| `GATUS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gatus
```

**Port conflict:**
Edit `.env` and change `GATUS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gatus ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gatus --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gatus_data:/data -v $(pwd):/backup alpine tar czf /backup/gatus-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gatus_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gatus-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gatus](https://github.com/twinproduction/gatus)
- **Docker Image:** `docker.io/twinproduction/gatus:latest`
- **Documentation:** [GitHub Wiki](https://github.com/twinproduction/gatus/wiki)
- **Issues:** [GitHub Issues](https://github.com/twinproduction/gatus/issues)

