---
title: "2Fauth"
description: "Self-hosted 2fauth deployment via Docker"
---

# 2Fauth

Self-hosted 2fauth deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/2fauth/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/2fauth/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/2fauth/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `2fauth` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5a7dc405968c62a19167950ca2a18c68fa2c9030177685ba4fc988267c04ef23` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `2fauth` | docker.io/2fauth/2fauth:latest | Main application service |
| `2fauth_data` | (volume) | Persistent data storage |

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
| `TWOFAUTH_PORT` | `8000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs 2fauth
```

**Port conflict:**
Edit `.env` and change `2FAUTH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec 2fauth ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect 2fauth --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v 2fauth_data:/data -v $(pwd):/backup alpine tar czf /backup/2fauth-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v 2fauth_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/2fauth-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [2Fauth](https://github.com/2fauth/2fauth)
- **Docker Image:** `docker.io/2fauth/2fauth:latest`
- **Documentation:** [GitHub Wiki](https://github.com/2fauth/2fauth/wiki)
- **Issues:** [GitHub Issues](https://github.com/2fauth/2fauth/issues)

