---
title: "Remmina"
description: "Self-hosted Remmina deployment via Docker"
---

# Remmina

Self-hosted Remmina deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/remmina/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/remmina/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/remmina/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `remmina` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `df49db701bb6ba37133862d091e6139bb291f8b4de80b07706d78ae03eb6b5dc` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `remmina` | docker.io/kasmweb/remmina:latest | Main application service |
| `remmina_data` | (volume) | Persistent data storage |

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
| `REMMINA_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs remmina
```

**Port conflict:**
Edit `.env` and change `REMMINA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec remmina ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect remmina --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v remmina_data:/data -v $(pwd):/backup alpine tar czf /backup/remmina-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v remmina_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/remmina-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Remmina](https://github.com/kasmweb/remmina)
- **Docker Image:** `docker.io/kasmweb/remmina:latest`
- **Documentation:** [GitHub Wiki](https://github.com/kasmweb/remmina/wiki)
- **Issues:** [GitHub Issues](https://github.com/kasmweb/remmina/issues)

