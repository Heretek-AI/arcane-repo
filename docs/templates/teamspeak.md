---
title: "Teamspeak"
description: "Self-hosted Teamspeak deployment via Docker"
---

# Teamspeak

Self-hosted Teamspeak deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/teamspeak/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/teamspeak/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/teamspeak/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `teamspeak` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `12c1d2239db7d9f253ae084a8670438a1c1267049e7d2015e64470f8c0b87095` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `teamspeak` | docker.io/library/teamspeak:latest | Main application service |
| `teamspeak_data` | (volume) | Persistent data storage |

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
| `TEAMSPEAK_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs teamspeak
```

**Port conflict:**
Edit `.env` and change `TEAMSPEAK_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec teamspeak ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect teamspeak --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v teamspeak_data:/data -v $(pwd):/backup alpine tar czf /backup/teamspeak-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v teamspeak_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/teamspeak-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Docker Image:** `docker.io/library/teamspeak:latest`

