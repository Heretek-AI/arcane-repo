---
title: "Clamav"
description: "Self-hosted Clamav deployment via Docker"
---

# Clamav

Self-hosted Clamav deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/clamav/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/clamav/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/clamav/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `clamav` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `60d46107a54bddb1c296a35ad0017d47cebb845fe576e93600b9d94b238cfb31` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `clamav` | docker.io/clamav/clamav:latest | Main application service |
| `clamav_data` | (volume) | Persistent data storage |

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
| `CLAMAV_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs clamav
```

**Port conflict:**
Edit `.env` and change `CLAMAV_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec clamav ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect clamav --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v clamav_data:/data -v $(pwd):/backup alpine tar czf /backup/clamav-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v clamav_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/clamav-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Clamav](https://github.com/clamav/clamav)
- **Docker Image:** `docker.io/clamav/clamav:latest`
- **Documentation:** [GitHub Wiki](https://github.com/clamav/clamav/wiki)
- **Issues:** [GitHub Issues](https://github.com/clamav/clamav/issues)

