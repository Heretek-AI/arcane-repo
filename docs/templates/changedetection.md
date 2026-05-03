---
title: "Changedetection"
description: "Self-hosted Changedetection deployment via Docker"
---

# Changedetection

Self-hosted Changedetection deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/changedetection/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/changedetection/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/changedetection/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `changedetection` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ca971b1af977925ade6647ed3601d243d357695dc51b4b71f02011d6adc0f324` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `changedetection` | docker.io/thib4ut/changedetection:latest | Main application service |
| `changedetection_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:5000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:5000](http://localhost:5000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `CHANGEDETECTION_PORT` | `5000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs changedetection
```

**Port conflict:**
Edit `.env` and change `CHANGEDETECTION_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec changedetection ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect changedetection --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v changedetection_data:/data -v $(pwd):/backup alpine tar czf /backup/changedetection-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v changedetection_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/changedetection-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Changedetection](https://github.com/thib4ut/changedetection)
- **Docker Image:** `docker.io/thib4ut/changedetection:latest`
- **Documentation:** [GitHub Wiki](https://github.com/thib4ut/changedetection/wiki)
- **Issues:** [GitHub Issues](https://github.com/thib4ut/changedetection/issues)

