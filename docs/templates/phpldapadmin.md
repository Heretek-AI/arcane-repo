---
title: "Phpldapadmin"
description: "Self-hosted Phpldapadmin deployment via Docker"
---

# Phpldapadmin

Self-hosted Phpldapadmin deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/phpldapadmin/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/phpldapadmin/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/phpldapadmin/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `phpldapadmin` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `f4ad7752583dac6f086df6f5519e75eecde0bc3f3dd79c60b9312cf6dd6ac4a0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `phpldapadmin` | docker.io/phpldapadmin/phpldapadmin:latest | Main application service |
| `phpldapadmin_data` | (volume) | Persistent data storage |

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
| `PHPLDAPADMIN_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs phpldapadmin
```

**Port conflict:**
Edit `.env` and change `PHPLDAPADMIN_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec phpldapadmin ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect phpldapadmin --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v phpldapadmin_data:/data -v $(pwd):/backup alpine tar czf /backup/phpldapadmin-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v phpldapadmin_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/phpldapadmin-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Phpldapadmin](https://github.com/phpldapadmin/phpldapadmin)
- **Docker Image:** `docker.io/phpldapadmin/phpldapadmin:latest`
- **Documentation:** [GitHub Wiki](https://github.com/phpldapadmin/phpldapadmin/wiki)
- **Issues:** [GitHub Issues](https://github.com/phpldapadmin/phpldapadmin/issues)

