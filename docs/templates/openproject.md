---
title: "Openproject"
description: "Self-hosted Openproject deployment via Docker"
---

# Openproject

Self-hosted Openproject deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openproject/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openproject/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openproject/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openproject` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ec5f54fadd33cce4653e33d136dc05c484df952ff4506c418a6acc6e3b479962` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `openproject` | docker.io/openproject/openproject:latest | Main application service |
| `openproject_data` | (volume) | Persistent data storage |

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
| `OPENPROJECT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs openproject
```

**Port conflict:**
Edit `.env` and change `OPENPROJECT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec openproject ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect openproject --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v openproject_data:/data -v $(pwd):/backup alpine tar czf /backup/openproject-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v openproject_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/openproject-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Openproject](https://github.com/openproject/openproject)
- **Docker Image:** `docker.io/openproject/openproject:latest`
- **Documentation:** [GitHub Wiki](https://github.com/openproject/openproject/wiki)
- **Issues:** [GitHub Issues](https://github.com/openproject/openproject/issues)

