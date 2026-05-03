---
title: "File Browser"
description: "Self-hosted File Browser deployment via Docker"
---

# File Browser

Self-hosted File Browser deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/storage" class="tag-badge">storage</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/file-browser/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/file-browser/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/file-browser/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `file-browser` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7d665cc1f81c41d0bad7c20cd5e7b9c35d07daf2bf38924e553ab695cbc90935` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `file-browser` | docker.io/krisss/file-browser:latest | Main application service |
| `file-browser_data` | (volume) | Persistent data storage |

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
| `FILE_BROWSER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs file-browser
```

**Port conflict:**
Edit `.env` and change `FILE-BROWSER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec file-browser ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect file-browser --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v file-browser_data:/data -v $(pwd):/backup alpine tar czf /backup/file-browser-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v file-browser_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/file-browser-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [File Browser](https://github.com/krisss/file-browser)
- **Docker Image:** `docker.io/krisss/file-browser:latest`
- **Documentation:** [GitHub Wiki](https://github.com/krisss/file-browser/wiki)
- **Issues:** [GitHub Issues](https://github.com/krisss/file-browser/issues)

