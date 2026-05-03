---
title: "Ojs"
description: "Self-hosted Ojs deployment via Docker"
---

# Ojs

Self-hosted Ojs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ojs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ojs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/ojs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `ojs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `28fa5acdfbb280a3bf683072fd6f7c8ba162e39281c364dc28cf3a768c084735` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `ojs` | docker.io/pkpofficial/ojs:latest | Main application service |
| `ojs_data` | (volume) | Persistent data storage |

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
| `OJS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs ojs
```

**Port conflict:**
Edit `.env` and change `OJS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec ojs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect ojs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v ojs_data:/data -v $(pwd):/backup alpine tar czf /backup/ojs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v ojs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/ojs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Ojs](https://github.com/pkpofficial/ojs)
- **Docker Image:** `docker.io/pkpofficial/ojs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/pkpofficial/ojs/wiki)
- **Issues:** [GitHub Issues](https://github.com/pkpofficial/ojs/issues)

