---
title: "Retroarch"
description: "Self-hosted Retroarch deployment via Docker"
---

# Retroarch

Self-hosted Retroarch deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/retroarch/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/retroarch/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/retroarch/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `retroarch` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d7e526d4b609373c89c7b390b5ae9a98c18e80f3f5508cffe4a39c7b4fccf748` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `retroarch` | docker.io/kasmweb/retroarch:latest | Main application service |
| `retroarch_data` | (volume) | Persistent data storage |

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
| `RETROARCH_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs retroarch
```

**Port conflict:**
Edit `.env` and change `RETROARCH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec retroarch ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect retroarch --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v retroarch_data:/data -v $(pwd):/backup alpine tar czf /backup/retroarch-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v retroarch_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/retroarch-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Retroarch](https://github.com/kasmweb/retroarch)
- **Docker Image:** `docker.io/kasmweb/retroarch:latest`
- **Documentation:** [GitHub Wiki](https://github.com/kasmweb/retroarch/wiki)
- **Issues:** [GitHub Issues](https://github.com/kasmweb/retroarch/issues)

