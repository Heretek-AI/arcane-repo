---
title: "Flatnotes"
description: "Self-hosted Flatnotes deployment via Docker"
---

# Flatnotes

Self-hosted Flatnotes deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flatnotes/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flatnotes/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flatnotes/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flatnotes` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `079392902ef16fcb9e250853cbecc5b20d5b7867168d108e39438037be40cb99` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `flatnotes` | docker.io/dullage/flatnotes:latest | Main application service |
| `flatnotes_data` | (volume) | Persistent data storage |

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
| `FLATNOTES_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs flatnotes
```

**Port conflict:**
Edit `.env` and change `FLATNOTES_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec flatnotes ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect flatnotes --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v flatnotes_data:/data -v $(pwd):/backup alpine tar czf /backup/flatnotes-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v flatnotes_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/flatnotes-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Flatnotes](https://github.com/dullage/flatnotes)
- **Docker Image:** `docker.io/dullage/flatnotes:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dullage/flatnotes/wiki)
- **Issues:** [GitHub Issues](https://github.com/dullage/flatnotes/issues)

