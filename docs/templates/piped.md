---
title: "Piped"
description: "Self-hosted Piped deployment via Docker"
---

# Piped

Self-hosted Piped deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/piped/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/piped/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/piped/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `piped` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d532964e5ae273822b5b7877186812201180494ccf7f2adf4e291482eaf96d13` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `piped` | docker.io/1337kavin/piped:latest | Main application service |
| `piped_data` | (volume) | Persistent data storage |

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
| `PIPED_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs piped
```

**Port conflict:**
Edit `.env` and change `PIPED_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec piped ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect piped --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v piped_data:/data -v $(pwd):/backup alpine tar czf /backup/piped-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v piped_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/piped-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Piped](https://github.com/1337kavin/piped)
- **Docker Image:** `docker.io/1337kavin/piped:latest`
- **Documentation:** [GitHub Wiki](https://github.com/1337kavin/piped/wiki)
- **Issues:** [GitHub Issues](https://github.com/1337kavin/piped/issues)

