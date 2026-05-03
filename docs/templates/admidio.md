---
title: "Admidio"
description: "Self-hosted Admidio deployment via Docker"
---

# Admidio

Self-hosted Admidio deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/admidio/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/admidio/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/admidio/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `admidio` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `684d805fb421a9f3a77188a911f9acc53c30ad37300c52bb1ab08a392b4b8dea` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `admidio` | docker.io/admidio/admidio:latest | Main application service |
| `admidio_data` | (volume) | Persistent data storage |

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
| `ADMIDIO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs admidio
```

**Port conflict:**
Edit `.env` and change `ADMIDIO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec admidio ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect admidio --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v admidio_data:/data -v $(pwd):/backup alpine tar czf /backup/admidio-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v admidio_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/admidio-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Admidio](https://github.com/admidio/admidio)
- **Docker Image:** `docker.io/admidio/admidio:latest`
- **Documentation:** [GitHub Wiki](https://github.com/admidio/admidio/wiki)
- **Issues:** [GitHub Issues](https://github.com/admidio/admidio/issues)

