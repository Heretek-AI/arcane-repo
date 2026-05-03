---
title: "Jam"
description: "Self-hosted Jam deployment via Docker"
---

# Jam

Self-hosted Jam deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jam/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jam/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/jam/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `jam` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `777d65fd210cb69057d5a802351b024ceb8c01a5d1c97f34c2f705cae9b393f3` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `jam` | docker.io/scrollagency/jam:latest | Main application service |
| `jam_data` | (volume) | Persistent data storage |

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
| `JAM_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs jam
```

**Port conflict:**
Edit `.env` and change `JAM_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec jam ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect jam --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v jam_data:/data -v $(pwd):/backup alpine tar czf /backup/jam-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v jam_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/jam-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Jam](https://github.com/scrollagency/jam)
- **Docker Image:** `docker.io/scrollagency/jam:latest`
- **Documentation:** [GitHub Wiki](https://github.com/scrollagency/jam/wiki)
- **Issues:** [GitHub Issues](https://github.com/scrollagency/jam/issues)

