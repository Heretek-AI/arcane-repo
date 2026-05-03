---
title: "Bitcoin Knots"
description: "Self-hosted Bitcoin Knots deployment via Docker"
---

# Bitcoin Knots

Self-hosted Bitcoin Knots deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bitcoin-knots/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bitcoin-knots/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bitcoin-knots/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bitcoin-knots` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `850e6a29e8a69ae9827f9cd88e25573725745f739d0e132841bdee5bfc7f7b42` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `bitcoin-knots` | ghcr.io/linuxserver/bitcoin-knots:latest | Main application service |
| `bitcoin-knots_data` | (volume) | Persistent data storage |

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
| `BITCOIN_KNOTS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs bitcoin-knots
```

**Port conflict:**
Edit `.env` and change `BITCOIN-KNOTS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec bitcoin-knots ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect bitcoin-knots --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v bitcoin-knots_data:/data -v $(pwd):/backup alpine tar czf /backup/bitcoin-knots-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v bitcoin-knots_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/bitcoin-knots-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Bitcoin Knots](https://github.com/linuxserver/bitcoin-knots)
- **Docker Image:** `ghcr.io/linuxserver/bitcoin-knots:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/bitcoin-knots/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/bitcoin-knots/issues)

