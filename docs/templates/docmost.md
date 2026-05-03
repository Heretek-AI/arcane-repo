---
title: "Docmost"
description: "Self-hosted Docmost deployment via Docker"
---

# Docmost

Self-hosted Docmost deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docmost/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docmost/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docmost/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `docmost` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5928b8d9bdc0d99d4defcfddcef601524f081cfb59f394b5d10efd7fae34f0a0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `docmost` | docker.io/docmost/docmost:latest | Main application service |
| `docmost_data` | (volume) | Persistent data storage |

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
| `DOCMOST_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs docmost
```

**Port conflict:**
Edit `.env` and change `DOCMOST_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec docmost ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect docmost --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v docmost_data:/data -v $(pwd):/backup alpine tar czf /backup/docmost-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v docmost_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/docmost-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Docmost](https://github.com/docmost/docmost)
- **Docker Image:** `docker.io/docmost/docmost:latest`
- **Documentation:** [GitHub Wiki](https://github.com/docmost/docmost/wiki)
- **Issues:** [GitHub Issues](https://github.com/docmost/docmost/issues)

