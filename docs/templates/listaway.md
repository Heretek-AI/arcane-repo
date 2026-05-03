---
title: "Listaway"
description: "Self-hosted Listaway deployment via Docker"
---

# Listaway

Self-hosted Listaway deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/listaway/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/listaway/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/listaway/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `listaway` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f92140bd6a64e60bbc352feefb4c2ed0227d4d12732fb168ef3a431adf97c180` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `listaway` | ghcr.io/jeffrpowell/listaway:latest | Main application service |
| `listaway_data` | (volume) | Persistent data storage |

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
| `LISTAWAY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs listaway
```

**Port conflict:**
Edit `.env` and change `LISTAWAY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec listaway ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect listaway --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v listaway_data:/data -v $(pwd):/backup alpine tar czf /backup/listaway-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v listaway_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/listaway-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Listaway](https://github.com/jeffrpowell/listaway)
- **Docker Image:** `ghcr.io/jeffrpowell/listaway:latest`
- **Documentation:** [GitHub Wiki](https://github.com/jeffrpowell/listaway/wiki)
- **Issues:** [GitHub Issues](https://github.com/jeffrpowell/listaway/issues)

