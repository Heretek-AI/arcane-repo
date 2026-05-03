---
title: "Mobilizon"
description: "Self-hosted Mobilizon deployment via Docker"
---

# Mobilizon

Self-hosted Mobilizon deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mobilizon/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mobilizon/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mobilizon/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mobilizon` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c6d00f970f986d3f1405a56201991ca6da261e7813e96261f2a2079baa19b99f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mobilizon` | docker.io/mobilizon/mobilizon:latest | Main application service |
| `mobilizon_data` | (volume) | Persistent data storage |

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
| `MOBILIZON_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mobilizon
```

**Port conflict:**
Edit `.env` and change `MOBILIZON_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mobilizon ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mobilizon --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mobilizon_data:/data -v $(pwd):/backup alpine tar czf /backup/mobilizon-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mobilizon_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mobilizon-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mobilizon](https://github.com/mobilizon/mobilizon)
- **Docker Image:** `docker.io/mobilizon/mobilizon:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mobilizon/mobilizon/wiki)
- **Issues:** [GitHub Issues](https://github.com/mobilizon/mobilizon/issues)

