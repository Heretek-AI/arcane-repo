---
title: "Conduit"
description: "Self-hosted Conduit deployment via Docker"
---

# Conduit

Self-hosted Conduit deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/conduit/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/conduit/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/conduit/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `conduit` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `76d67b4fb6dc28abe7ab5b449314e85ace9168509f55a27029dea1a4c1b2b75f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `conduit` | docker.io/freedom4iran/conduit:latest | Main application service |
| `conduit_data` | (volume) | Persistent data storage |

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
| `CONDUIT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs conduit
```

**Port conflict:**
Edit `.env` and change `CONDUIT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec conduit ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect conduit --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v conduit_data:/data -v $(pwd):/backup alpine tar czf /backup/conduit-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v conduit_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/conduit-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Conduit](https://github.com/freedom4iran/conduit)
- **Docker Image:** `docker.io/freedom4iran/conduit:latest`
- **Documentation:** [GitHub Wiki](https://github.com/freedom4iran/conduit/wiki)
- **Issues:** [GitHub Issues](https://github.com/freedom4iran/conduit/issues)

