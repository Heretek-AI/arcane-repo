---
title: "Diaspora"
description: "Self-hosted Diaspora deployment via Docker"
---

# Diaspora

Self-hosted Diaspora deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/diaspora/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/diaspora/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/diaspora/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `diaspora` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d6f8796fb483ec3a4e3edd6e20c52b69db96af9356f6aa24a5f1b489cafe4cd0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `diaspora` | docker.io/koehn/diaspora:latest | Main application service |
| `diaspora_data` | (volume) | Persistent data storage |

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
| `DIASPORA_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs diaspora
```

**Port conflict:**
Edit `.env` and change `DIASPORA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec diaspora ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect diaspora --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v diaspora_data:/data -v $(pwd):/backup alpine tar czf /backup/diaspora-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v diaspora_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/diaspora-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Diaspora](https://github.com/koehn/diaspora)
- **Docker Image:** `docker.io/koehn/diaspora:latest`
- **Documentation:** [GitHub Wiki](https://github.com/koehn/diaspora/wiki)
- **Issues:** [GitHub Issues](https://github.com/koehn/diaspora/issues)

