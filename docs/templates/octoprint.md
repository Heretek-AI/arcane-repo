---
title: "Octoprint"
description: "Self-hosted Octoprint deployment via Docker"
---

# Octoprint

Self-hosted Octoprint deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/octoprint/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/octoprint/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/octoprint/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `octoprint` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8df4b13e000896c816e29079d38573c974777b09b3480201ee419366b783ec79` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `octoprint` | docker.io/octoprint/octoprint:latest | Main application service |
| `octoprint_data` | (volume) | Persistent data storage |

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
| `OCTOPRINT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs octoprint
```

**Port conflict:**
Edit `.env` and change `OCTOPRINT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec octoprint ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect octoprint --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v octoprint_data:/data -v $(pwd):/backup alpine tar czf /backup/octoprint-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v octoprint_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/octoprint-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Octoprint](https://github.com/octoprint/octoprint)
- **Docker Image:** `docker.io/octoprint/octoprint:latest`
- **Documentation:** [GitHub Wiki](https://github.com/octoprint/octoprint/wiki)
- **Issues:** [GitHub Issues](https://github.com/octoprint/octoprint/issues)

