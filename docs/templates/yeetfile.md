---
title: "Yeetfile"
description: "Self-hosted Yeetfile deployment via Docker"
---

# Yeetfile

Self-hosted Yeetfile deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/storage" class="tag-badge">storage</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yeetfile/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yeetfile/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yeetfile/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `yeetfile` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1260087a571a73784b4fafa375e24cc713f08bc24a1d924b746bfc664a4842e9` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `yeetfile` | ghcr.io/benbusby/yeetfile:latest | Main application service |
| `yeetfile_data` | (volume) | Persistent data storage |

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
| `YEETFILE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs yeetfile
```

**Port conflict:**
Edit `.env` and change `YEETFILE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec yeetfile ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect yeetfile --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v yeetfile_data:/data -v $(pwd):/backup alpine tar czf /backup/yeetfile-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v yeetfile_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/yeetfile-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Yeetfile](https://github.com/benbusby/yeetfile)
- **Docker Image:** `ghcr.io/benbusby/yeetfile:latest`
- **Documentation:** [GitHub Wiki](https://github.com/benbusby/yeetfile/wiki)
- **Issues:** [GitHub Issues](https://github.com/benbusby/yeetfile/issues)

