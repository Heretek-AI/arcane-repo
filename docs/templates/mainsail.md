---
title: "Mainsail"
description: "Self-hosted Mainsail deployment via Docker"
---

# Mainsail

Self-hosted Mainsail deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mainsail/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mainsail/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mainsail/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mainsail` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `034db74c448bf46781333f5409004186371a56221f0385fe8411c28cabed2ae8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `mainsail` | docker.io/dimalo/mainsail:latest | Main application service |
| `mainsail_data` | (volume) | Persistent data storage |

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
| `MAINSAIL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs mainsail
```

**Port conflict:**
Edit `.env` and change `MAINSAIL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec mainsail ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect mainsail --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v mainsail_data:/data -v $(pwd):/backup alpine tar czf /backup/mainsail-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v mainsail_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/mainsail-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Mainsail](https://github.com/dimalo/mainsail)
- **Docker Image:** `docker.io/dimalo/mainsail:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dimalo/mainsail/wiki)
- **Issues:** [GitHub Issues](https://github.com/dimalo/mainsail/issues)

