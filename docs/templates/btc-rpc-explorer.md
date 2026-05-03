---
title: "Btc Rpc Explorer"
description: "Self-hosted Btc Rpc Explorer deployment via Docker"
---

# Btc Rpc Explorer

Self-hosted Btc Rpc Explorer deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/btc-rpc-explorer/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/btc-rpc-explorer/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/btc-rpc-explorer/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `btc-rpc-explorer` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `87ed7f630911f40728cb354c305dfb498b703a0aea4648623bb7c931041a1a31` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `btc-rpc-explorer` | docker.io/getumbrel/btc-rpc-explorer:latest | Main application service |
| `btc-rpc-explorer_data` | (volume) | Persistent data storage |

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
| `BTC_RPC_EXPLORER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs btc-rpc-explorer
```

**Port conflict:**
Edit `.env` and change `BTC-RPC-EXPLORER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec btc-rpc-explorer ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect btc-rpc-explorer --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v btc-rpc-explorer_data:/data -v $(pwd):/backup alpine tar czf /backup/btc-rpc-explorer-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v btc-rpc-explorer_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/btc-rpc-explorer-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Btc Rpc Explorer](https://github.com/getumbrel/btc-rpc-explorer)
- **Docker Image:** `docker.io/getumbrel/btc-rpc-explorer:latest`
- **Documentation:** [GitHub Wiki](https://github.com/getumbrel/btc-rpc-explorer/wiki)
- **Issues:** [GitHub Issues](https://github.com/getumbrel/btc-rpc-explorer/issues)

