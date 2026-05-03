---
title: "Open Webui"
description: "Self-hosted Open Webui deployment via Docker"
---

# Open Webui

Self-hosted Open Webui deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/open-webui/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/open-webui/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/open-webui/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `open-webui` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d9aa620f139a97581d22cf9f9ab1ab65e5369ba77a3c64b7934c1866e45704fc` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `open-webui` | ghcr.io/open-webui/open-webui:latest | Main application service |
| `open-webui_data` | (volume) | Persistent data storage |

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
| `OPEN_WEBUI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs open-webui
```

**Port conflict:**
Edit `.env` and change `OPEN-WEBUI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec open-webui ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect open-webui --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v open-webui_data:/data -v $(pwd):/backup alpine tar czf /backup/open-webui-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v open-webui_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/open-webui-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Open Webui](https://github.com/open-webui/open-webui)
- **Docker Image:** `ghcr.io/open-webui/open-webui:latest`
- **Documentation:** [GitHub Wiki](https://github.com/open-webui/open-webui/wiki)
- **Issues:** [GitHub Issues](https://github.com/open-webui/open-webui/issues)

