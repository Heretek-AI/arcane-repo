---
title: "Holesail Switchboard"
description: "Self-hosted Holesail Switchboard deployment via Docker"
---

# Holesail Switchboard

Self-hosted Holesail Switchboard deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/holesail-switchboard/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/holesail-switchboard/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/holesail-switchboard/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `holesail-switchboard` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ff03d6ca973366892ef168d564ef100d9ead65648e5f17d42ec1fc6439a0bad8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `holesail-switchboard` | docker.io/orenz0/holesail-switchboard:latest | Main application service |
| `holesail-switchboard_data` | (volume) | Persistent data storage |

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
| `HOLESAIL_SWITCHBOARD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs holesail-switchboard
```

**Port conflict:**
Edit `.env` and change `HOLESAIL-SWITCHBOARD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec holesail-switchboard ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect holesail-switchboard --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v holesail-switchboard_data:/data -v $(pwd):/backup alpine tar czf /backup/holesail-switchboard-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v holesail-switchboard_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/holesail-switchboard-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Holesail Switchboard](https://github.com/orenz0/holesail-switchboard)
- **Docker Image:** `docker.io/orenz0/holesail-switchboard:latest`
- **Documentation:** [GitHub Wiki](https://github.com/orenz0/holesail-switchboard/wiki)
- **Issues:** [GitHub Issues](https://github.com/orenz0/holesail-switchboard/issues)

