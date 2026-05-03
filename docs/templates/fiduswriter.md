---
title: "Fiduswriter"
description: "Self-hosted Fiduswriter deployment via Docker"
---

# Fiduswriter

Self-hosted Fiduswriter deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fiduswriter/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fiduswriter/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fiduswriter/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `fiduswriter` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `0c508f41c8a77a131029f2289432a071891dc10f70f55fa4e6777c34d2518160` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `fiduswriter` | docker.io/fiduswriter/fiduswriter:latest | Main application service |
| `fiduswriter_data` | (volume) | Persistent data storage |

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
| `FIDUSWRITER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs fiduswriter
```

**Port conflict:**
Edit `.env` and change `FIDUSWRITER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fiduswriter ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fiduswriter --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fiduswriter_data:/data -v $(pwd):/backup alpine tar czf /backup/fiduswriter-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fiduswriter_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fiduswriter-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Fiduswriter](https://github.com/fiduswriter/fiduswriter)
- **Docker Image:** `docker.io/fiduswriter/fiduswriter:latest`
- **Documentation:** [GitHub Wiki](https://github.com/fiduswriter/fiduswriter/wiki)
- **Issues:** [GitHub Issues](https://github.com/fiduswriter/fiduswriter/issues)

