---
title: "Qui"
description: "Self-hosted Qui deployment via Docker"
---

# Qui

Self-hosted Qui deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/qui/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/qui/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/qui/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `qui` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `76e49f93af02db53014ab9c1c9aceb7f090b13703be4e8e2f81f9d2f6a8dd56e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `qui` | docker.io/fvboegeld/qui:latest | Main application service |
| `qui_data` | (volume) | Persistent data storage |

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
| `QUI_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs qui
```

**Port conflict:**
Edit `.env` and change `QUI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec qui ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect qui --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v qui_data:/data -v $(pwd):/backup alpine tar czf /backup/qui-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v qui_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/qui-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Qui](https://github.com/fvboegeld/qui)
- **Docker Image:** `docker.io/fvboegeld/qui:latest`
- **Documentation:** [GitHub Wiki](https://github.com/fvboegeld/qui/wiki)
- **Issues:** [GitHub Issues](https://github.com/fvboegeld/qui/issues)

