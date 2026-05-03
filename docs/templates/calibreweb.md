---
title: "Calibreweb"
description: "Self-hosted Calibreweb deployment via Docker"
---

# Calibreweb

Self-hosted Calibreweb deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/calibreweb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/calibreweb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/calibreweb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `calibreweb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f596ed1bef763cd601fd6b3e9948c68497bd799bc62f03b7b823d4a2fae6b703` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `calibreweb` | docker.io/fluffybacon/calibreweb:latest | Main application service |
| `calibreweb_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8083/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8083](http://localhost:8083) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `CALIBREWEB_PORT` | `8083` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs calibreweb
```

**Port conflict:**
Edit `.env` and change `CALIBREWEB_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec calibreweb ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect calibreweb --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v calibreweb_data:/data -v $(pwd):/backup alpine tar czf /backup/calibreweb-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v calibreweb_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/calibreweb-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Calibreweb](https://github.com/fluffybacon/calibreweb)
- **Docker Image:** `docker.io/fluffybacon/calibreweb:latest`
- **Documentation:** [GitHub Wiki](https://github.com/fluffybacon/calibreweb/wiki)
- **Issues:** [GitHub Issues](https://github.com/fluffybacon/calibreweb/issues)

