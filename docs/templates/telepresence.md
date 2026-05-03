---
title: "Telepresence"
description: "Self-hosted Telepresence deployment via Docker"
---

# Telepresence

Self-hosted Telepresence deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/priority" class="tag-badge">priority</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/telepresence/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/telepresence/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/telepresence/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `telepresence` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `956edbf43c5cb5619ed73f24f719bad719ef0f52514d1908a3c36438fc44f6f5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `telepresence` | ghcr.io/telepresenceio/telepresence:latest | Main application service |
| `telepresence_data` | (volume) | Persistent data storage |

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
| `TELEPRESENCE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs telepresence
```

**Port conflict:**
Edit `.env` and change `TELEPRESENCE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec telepresence ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect telepresence --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v telepresence_data:/data -v $(pwd):/backup alpine tar czf /backup/telepresence-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v telepresence_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/telepresence-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Telepresence](https://github.com/telepresenceio/telepresence)
- **Docker Image:** `ghcr.io/telepresenceio/telepresence:latest`
- **Documentation:** [GitHub Wiki](https://github.com/telepresenceio/telepresence/wiki)
- **Issues:** [GitHub Issues](https://github.com/telepresenceio/telepresence/issues)

