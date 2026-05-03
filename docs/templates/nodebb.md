---
title: "Nodebb"
description: "Self-hosted Nodebb deployment via Docker"
---

# Nodebb

Self-hosted Nodebb deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nodebb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nodebb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nodebb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `nodebb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `99f39a9994330c49366c9ba4b2948323ebb0264651d25c19ee13ab42adfac362` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `nodebb` | ghcr.io/nodebb/nodebb:latest | Main application service |
| `nodebb_data` | (volume) | Persistent data storage |

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
| `NODEBB_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs nodebb
```

**Port conflict:**
Edit `.env` and change `NODEBB_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec nodebb ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect nodebb --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v nodebb_data:/data -v $(pwd):/backup alpine tar czf /backup/nodebb-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v nodebb_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/nodebb-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Nodebb](https://github.com/nodebb/nodebb)
- **Docker Image:** `ghcr.io/nodebb/nodebb:latest`
- **Documentation:** [GitHub Wiki](https://github.com/nodebb/nodebb/wiki)
- **Issues:** [GitHub Issues](https://github.com/nodebb/nodebb/issues)

