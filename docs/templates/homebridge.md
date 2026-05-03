---
title: "Homebridge"
description: "Self-hosted Homebridge deployment via Docker"
---

# Homebridge

Self-hosted Homebridge deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homebridge/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homebridge/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/homebridge/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `homebridge` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `757bfa61f86a7250799c999690734ff632fbf43e2c856fcc3462910ec0480a93` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `homebridge` | ghcr.io/homebridge/homebridge:latest | Main application service |
| `homebridge_data` | (volume) | Persistent data storage |

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
| `HOMEBRIDGE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs homebridge
```

**Port conflict:**
Edit `.env` and change `HOMEBRIDGE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec homebridge ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect homebridge --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v homebridge_data:/data -v $(pwd):/backup alpine tar czf /backup/homebridge-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v homebridge_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/homebridge-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Homebridge](https://github.com/homebridge/homebridge)
- **Docker Image:** `ghcr.io/homebridge/homebridge:latest`
- **Documentation:** [GitHub Wiki](https://github.com/homebridge/homebridge/wiki)
- **Issues:** [GitHub Issues](https://github.com/homebridge/homebridge/issues)

