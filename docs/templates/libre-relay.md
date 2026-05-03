---
title: "Libre Relay"
description: "Self-hosted Libre Relay deployment via Docker"
---

# Libre Relay

Self-hosted Libre Relay deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/libre-relay/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/libre-relay/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/libre-relay/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `libre-relay` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b0d12cc001026ed19c86ea2a3f04f5412a1bea37663f139ef4a1438a402365ad` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `libre-relay` | docker.io/levinster82/libre-relay:latest | Main application service |
| `libre-relay_data` | (volume) | Persistent data storage |

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
| `LIBRE_RELAY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs libre-relay
```

**Port conflict:**
Edit `.env` and change `LIBRE-RELAY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec libre-relay ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect libre-relay --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v libre-relay_data:/data -v $(pwd):/backup alpine tar czf /backup/libre-relay-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v libre-relay_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/libre-relay-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Libre Relay](https://github.com/levinster82/libre-relay)
- **Docker Image:** `docker.io/levinster82/libre-relay:latest`
- **Documentation:** [GitHub Wiki](https://github.com/levinster82/libre-relay/wiki)
- **Issues:** [GitHub Issues](https://github.com/levinster82/libre-relay/issues)

