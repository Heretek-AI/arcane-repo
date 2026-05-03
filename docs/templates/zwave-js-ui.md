---
title: "Zwave Js Ui"
description: "Self-hosted Zwave Js Ui deployment via Docker"
---

# Zwave Js Ui

Self-hosted Zwave Js Ui deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/zwave-js-ui/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/zwave-js-ui/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/zwave-js-ui/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `zwave-js-ui` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b7b57e3f7ee93cd3dbed180e2a56e11d576206403764d0a3c11eca3468358e3b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `zwave-js-ui` | docker.io/zwavejs/zwave-js-ui:latest | Main application service |
| `zwave-js-ui_data` | (volume) | Persistent data storage |

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
| `ZWAVE_JS_UI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs zwave-js-ui
```

**Port conflict:**
Edit `.env` and change `ZWAVE-JS-UI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec zwave-js-ui ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect zwave-js-ui --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v zwave-js-ui_data:/data -v $(pwd):/backup alpine tar czf /backup/zwave-js-ui-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v zwave-js-ui_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/zwave-js-ui-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Zwave Js Ui](https://github.com/zwavejs/zwave-js-ui)
- **Docker Image:** `docker.io/zwavejs/zwave-js-ui:latest`
- **Documentation:** [GitHub Wiki](https://github.com/zwavejs/zwave-js-ui/wiki)
- **Issues:** [GitHub Issues](https://github.com/zwavejs/zwave-js-ui/issues)

