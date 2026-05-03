---
title: "Cyberchef"
description: "Self-hosted Cyberchef deployment via Docker"
---

# Cyberchef

Self-hosted Cyberchef deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cyberchef/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cyberchef/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cyberchef/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cyberchef` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ea2f0021acec47087f4821af2043d0d933a369b8927f3bd4143638be478214b2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cyberchef` | docker.io/mpepping/cyberchef:latest | Main application service |
| `cyberchef_data` | (volume) | Persistent data storage |

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
| `CYBERCHEF_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cyberchef
```

**Port conflict:**
Edit `.env` and change `CYBERCHEF_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cyberchef ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cyberchef --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cyberchef_data:/data -v $(pwd):/backup alpine tar czf /backup/cyberchef-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cyberchef_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cyberchef-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cyberchef](https://github.com/mpepping/cyberchef)
- **Docker Image:** `docker.io/mpepping/cyberchef:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mpepping/cyberchef/wiki)
- **Issues:** [GitHub Issues](https://github.com/mpepping/cyberchef/issues)

