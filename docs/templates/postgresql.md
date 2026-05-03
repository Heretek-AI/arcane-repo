---
title: "Postgresql"
description: "Self-hosted Postgresql deployment via Docker"
---

# Postgresql

Self-hosted Postgresql deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/postgresql/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/postgresql/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/postgresql/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `postgresql` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `53e7a0db5cab0694a13ef1f0af2b28f9a21738ae38a7219e26df58f50a04a7a4` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `postgresql` | docker.io/bitnami/postgresql:latest | Main application service |
| `postgresql_data` | (volume) | Persistent data storage |

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
| `POSTGRESQL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs postgresql
```

**Port conflict:**
Edit `.env` and change `POSTGRESQL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec postgresql ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect postgresql --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v postgresql_data:/data -v $(pwd):/backup alpine tar czf /backup/postgresql-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v postgresql_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/postgresql-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Postgresql](https://github.com/bitnami/postgresql)
- **Docker Image:** `docker.io/bitnami/postgresql:latest`
- **Documentation:** [GitHub Wiki](https://github.com/bitnami/postgresql/wiki)
- **Issues:** [GitHub Issues](https://github.com/bitnami/postgresql/issues)

