---
title: "Peer Calls"
description: "Self-hosted Peer Calls deployment via Docker"
---

# Peer Calls

Self-hosted Peer Calls deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/peer-calls/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/peer-calls/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/peer-calls/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `peer-calls` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7f9388ac39dac45fc398e2121cde02217a2fc73290e718b8f42dd948b920bc86` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `peer-calls` | ghcr.io/peer-calls/peer-calls:latest | Main application service |
| `peer-calls_data` | (volume) | Persistent data storage |

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
| `PEER_CALLS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs peer-calls
```

**Port conflict:**
Edit `.env` and change `PEER-CALLS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec peer-calls ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect peer-calls --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v peer-calls_data:/data -v $(pwd):/backup alpine tar czf /backup/peer-calls-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v peer-calls_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/peer-calls-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Peer Calls](https://github.com/peer-calls/peer-calls)
- **Docker Image:** `ghcr.io/peer-calls/peer-calls:latest`
- **Documentation:** [GitHub Wiki](https://github.com/peer-calls/peer-calls/wiki)
- **Issues:** [GitHub Issues](https://github.com/peer-calls/peer-calls/issues)

