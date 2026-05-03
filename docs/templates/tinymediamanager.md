---
title: "Tinymediamanager"
description: "Self-hosted Tinymediamanager deployment via Docker"
---

# Tinymediamanager

Self-hosted Tinymediamanager deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tinymediamanager/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tinymediamanager/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tinymediamanager/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tinymediamanager` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `07c68ed49d302fd8c9d4234007782666f1351025316a54117e4dfe64a2439bea` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `tinymediamanager` | docker.io/tinymediamanager/tinymediamanager:latest | Main application service |
| `tinymediamanager_data` | (volume) | Persistent data storage |

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
| `TINYMEDIAMANAGER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs tinymediamanager
```

**Port conflict:**
Edit `.env` and change `TINYMEDIAMANAGER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec tinymediamanager ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect tinymediamanager --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v tinymediamanager_data:/data -v $(pwd):/backup alpine tar czf /backup/tinymediamanager-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v tinymediamanager_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/tinymediamanager-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Tinymediamanager](https://github.com/tinymediamanager/tinymediamanager)
- **Docker Image:** `docker.io/tinymediamanager/tinymediamanager:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tinymediamanager/tinymediamanager/wiki)
- **Issues:** [GitHub Issues](https://github.com/tinymediamanager/tinymediamanager/issues)

