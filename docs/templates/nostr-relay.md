---
title: "Nostr Relay"
description: "Self-hosted Nostr Relay deployment via Docker"
---

# Nostr Relay

Self-hosted Nostr Relay deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nostr-relay/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nostr-relay/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nostr-relay/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `nostr-relay` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d755768c5fe6983158da2bea66ed15e30d40f1947481e069a67bb465edf7e223` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `nostr-relay` | ghcr.io/mattn/nostr-relay:latest | Main application service |
| `nostr-relay_data` | (volume) | Persistent data storage |

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
| `NOSTR_RELAY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs nostr-relay
```

**Port conflict:**
Edit `.env` and change `NOSTR-RELAY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec nostr-relay ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect nostr-relay --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v nostr-relay_data:/data -v $(pwd):/backup alpine tar czf /backup/nostr-relay-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v nostr-relay_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/nostr-relay-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Nostr Relay](https://github.com/mattn/nostr-relay)
- **Docker Image:** `ghcr.io/mattn/nostr-relay:latest`
- **Documentation:** [GitHub Wiki](https://github.com/mattn/nostr-relay/wiki)
- **Issues:** [GitHub Issues](https://github.com/mattn/nostr-relay/issues)

