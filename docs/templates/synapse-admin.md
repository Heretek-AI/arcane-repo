---
title: "Synapse Admin"
description: "Self-hosted Synapse Admin deployment via Docker"
---

# Synapse Admin

Self-hosted Synapse Admin deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/synapse-admin/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/synapse-admin/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/synapse-admin/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `synapse-admin` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `e92a6cbeff05c604fcd8c4127c2b7a0111c903c08bde3ccd94fa6deb96f1022e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `synapse-admin` | docker.io/awesometechnologies/synapse-admin:latest | Main application service |
| `synapse-admin_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8008/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8008](http://localhost:8008) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNAPSE_ADMIN_PORT` | `8008` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs synapse-admin
```

**Port conflict:**
Edit `.env` and change `SYNAPSE-ADMIN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec synapse-admin ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect synapse-admin --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v synapse-admin_data:/data -v $(pwd):/backup alpine tar czf /backup/synapse-admin-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v synapse-admin_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/synapse-admin-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Synapse Admin](https://github.com/awesometechnologies/synapse-admin)
- **Docker Image:** `docker.io/awesometechnologies/synapse-admin:latest`
- **Documentation:** [GitHub Wiki](https://github.com/awesometechnologies/synapse-admin/wiki)
- **Issues:** [GitHub Issues](https://github.com/awesometechnologies/synapse-admin/issues)

