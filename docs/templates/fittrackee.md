---
title: "Fittrackee"
description: "Self-hosted Fittrackee deployment via Docker"
---

# Fittrackee

Self-hosted Fittrackee deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fittrackee/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fittrackee/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fittrackee/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `fittrackee` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d808881bb29a89b675c2f027ea8aca4cd4d416be83e47f5a648b99b61fad013b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `fittrackee` | docker.io/fittrackee/fittrackee:latest | Main application service |
| `fittrackee_data` | (volume) | Persistent data storage |

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
| `FITTRACKEE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs fittrackee
```

**Port conflict:**
Edit `.env` and change `FITTRACKEE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fittrackee ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fittrackee --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fittrackee_data:/data -v $(pwd):/backup alpine tar czf /backup/fittrackee-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fittrackee_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fittrackee-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Fittrackee](https://github.com/fittrackee/fittrackee)
- **Docker Image:** `docker.io/fittrackee/fittrackee:latest`
- **Documentation:** [GitHub Wiki](https://github.com/fittrackee/fittrackee/wiki)
- **Issues:** [GitHub Issues](https://github.com/fittrackee/fittrackee/issues)

