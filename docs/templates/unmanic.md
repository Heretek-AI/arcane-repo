---
title: "Unmanic"
description: "Self-hosted Unmanic deployment via Docker"
---

# Unmanic

Self-hosted Unmanic deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/unmanic/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/unmanic/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/unmanic/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `unmanic` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ac47bbd10075052ac48baad4c33f871d43aba6e0dcc7f27b332027e7270db820` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `unmanic` | ghcr.io/unmanic/unmanic:latest | Main application service |
| `unmanic_data` | (volume) | Persistent data storage |

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
| `UNMANIC_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs unmanic
```

**Port conflict:**
Edit `.env` and change `UNMANIC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec unmanic ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect unmanic --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v unmanic_data:/data -v $(pwd):/backup alpine tar czf /backup/unmanic-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v unmanic_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/unmanic-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Unmanic](https://github.com/unmanic/unmanic)
- **Docker Image:** `ghcr.io/unmanic/unmanic:latest`
- **Documentation:** [GitHub Wiki](https://github.com/unmanic/unmanic/wiki)
- **Issues:** [GitHub Issues](https://github.com/unmanic/unmanic/issues)

