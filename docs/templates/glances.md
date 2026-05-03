---
title: "Glances"
description: "Self-hosted Glances deployment via Docker"
---

# Glances

Self-hosted Glances deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/glances/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/glances/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/glances/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `glances` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6e3d29825b6027ee875ecffe896a0bf0f07761a2e69b6efc0875f9c2a0681673` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `glances` | docker.io/nicolargo/glances:latest | Main application service |
| `glances_data` | (volume) | Persistent data storage |

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
| `GLANCES_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs glances
```

**Port conflict:**
Edit `.env` and change `GLANCES_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec glances ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect glances --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v glances_data:/data -v $(pwd):/backup alpine tar czf /backup/glances-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v glances_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/glances-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Glances](https://github.com/nicolargo/glances)
- **Docker Image:** `docker.io/nicolargo/glances:latest`
- **Documentation:** [GitHub Wiki](https://github.com/nicolargo/glances/wiki)
- **Issues:** [GitHub Issues](https://github.com/nicolargo/glances/issues)

