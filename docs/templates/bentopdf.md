---
title: "Bentopdf"
description: "Self-hosted Bentopdf deployment via Docker"
---

# Bentopdf

Self-hosted Bentopdf deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bentopdf/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bentopdf/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bentopdf/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bentopdf` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c8372b00fa5fdad898c937ad271023d0c5910984984dd0c374abf5138eff2072` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `bentopdf` | docker.io/bentopdf/bentopdf:latest | Main application service |
| `bentopdf_data` | (volume) | Persistent data storage |

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
| `BENTOPDF_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs bentopdf
```

**Port conflict:**
Edit `.env` and change `BENTOPDF_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec bentopdf ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect bentopdf --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v bentopdf_data:/data -v $(pwd):/backup alpine tar czf /backup/bentopdf-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v bentopdf_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/bentopdf-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Bentopdf](https://github.com/bentopdf/bentopdf)
- **Docker Image:** `docker.io/bentopdf/bentopdf:latest`
- **Documentation:** [GitHub Wiki](https://github.com/bentopdf/bentopdf/wiki)
- **Issues:** [GitHub Issues](https://github.com/bentopdf/bentopdf/issues)

