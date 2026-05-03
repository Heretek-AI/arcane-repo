---
title: "Wikimore"
description: "Self-hosted Wikimore deployment via Docker"
---

# Wikimore

Self-hosted Wikimore deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikimore/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikimore/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikimore/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `wikimore` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `36ea6b43347ace06e42e8d6bdbe2b931293f98fed96bc822d13f7ee283c4dd32` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `wikimore` | docker.io/tlan16/wikimore:latest | Main application service |
| `wikimore_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:80/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:80](http://localhost:80) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WIKIMORE_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs wikimore
```

**Port conflict:**
Edit `.env` and change `WIKIMORE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec wikimore ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect wikimore --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v wikimore_data:/data -v $(pwd):/backup alpine tar czf /backup/wikimore-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v wikimore_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/wikimore-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Wikimore](https://github.com/tlan16/wikimore)
- **Docker Image:** `docker.io/tlan16/wikimore:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tlan16/wikimore/wiki)
- **Issues:** [GitHub Issues](https://github.com/tlan16/wikimore/issues)

