---
title: "Airtrail"
description: "Self-hosted Airtrail deployment via Docker"
---

# Airtrail

Self-hosted Airtrail deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/airtrail/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/airtrail/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/airtrail/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `airtrail` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1e14b9e3da33f4d27e8282231b6f6d84e595f2f7bce54747697461eeffb12fc6` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `airtrail` | docker.io/johly/airtrail:latest | Main application service |
| `airtrail_data` | (volume) | Persistent data storage |

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
| `AIRTRAIL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs airtrail
```

**Port conflict:**
Edit `.env` and change `AIRTRAIL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec airtrail ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect airtrail --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v airtrail_data:/data -v $(pwd):/backup alpine tar czf /backup/airtrail-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v airtrail_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/airtrail-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Airtrail](https://github.com/johly/airtrail)
- **Docker Image:** `docker.io/johly/airtrail:latest`
- **Documentation:** [GitHub Wiki](https://github.com/johly/airtrail/wiki)
- **Issues:** [GitHub Issues](https://github.com/johly/airtrail/issues)

