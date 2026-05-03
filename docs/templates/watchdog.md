---
title: "Watchdog"
description: "Self-hosted Watchdog deployment via Docker"
---

# Watchdog

Self-hosted Watchdog deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/watchdog/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/watchdog/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/watchdog/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `watchdog` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9cb63bc290745401c2893f1bf3eaf21022739aa03c5121d8ef19b35332f7d652` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `watchdog` | ghcr.io/mailcow/watchdog:latest | Main application service |
| `watchdog_data` | (volume) | Persistent data storage |

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
| `WATCHDOG_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs watchdog
```

**Port conflict:**
Edit `.env` and change `WATCHDOG_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec watchdog ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect watchdog --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v watchdog_data:/data -v $(pwd):/backup alpine tar czf /backup/watchdog-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v watchdog_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/watchdog-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Watchdog](https://github.com/mailcow/watchdog)
- **Docker Image:** `ghcr.io/mailcow/watchdog:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mailcow/watchdog/wiki)
- **Issues:** [GitHub Issues](https://github.com/mailcow/watchdog/issues)

