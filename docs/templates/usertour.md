---
title: "Usertour"
description: "Self-hosted Usertour deployment via Docker"
---

# Usertour

Self-hosted Usertour deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/usertour/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/usertour/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/usertour/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `usertour` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `2050a1efed682e34851e6fee4d961e250b405dddc71707852fa70c0213b5217c` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `usertour` | docker.io/usertour/usertour:latest | Main application service |
| `usertour_data` | (volume) | Persistent data storage |

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
| `USERTOUR_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs usertour
```

**Port conflict:**
Edit `.env` and change `USERTOUR_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec usertour ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect usertour --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v usertour_data:/data -v $(pwd):/backup alpine tar czf /backup/usertour-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v usertour_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/usertour-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Usertour](https://github.com/usertour/usertour)
- **Docker Image:** `docker.io/usertour/usertour:latest`
- **Documentation:** [GitHub Wiki](https://github.com/usertour/usertour/wiki)
- **Issues:** [GitHub Issues](https://github.com/usertour/usertour/issues)

