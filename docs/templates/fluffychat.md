---
title: "Fluffychat"
description: "Self-hosted Fluffychat deployment via Docker"
---

# Fluffychat

Self-hosted Fluffychat deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/communication" class="tag-badge">communication</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fluffychat/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fluffychat/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/fluffychat/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `fluffychat` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `2c24b799c09446411effbe8577299ab171037d14e5680cc7668c9f80e08d0c79` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `fluffychat` | ghcr.io/aceberg/fluffychat:latest | Main application service |
| `fluffychat_data` | (volume) | Persistent data storage |

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
| `FLUFFYCHAT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs fluffychat
```

**Port conflict:**
Edit `.env` and change `FLUFFYCHAT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec fluffychat ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect fluffychat --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v fluffychat_data:/data -v $(pwd):/backup alpine tar czf /backup/fluffychat-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v fluffychat_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/fluffychat-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Fluffychat](https://github.com/aceberg/fluffychat)
- **Docker Image:** `ghcr.io/aceberg/fluffychat:latest`
- **Documentation:** [GitHub Wiki](https://github.com/aceberg/fluffychat/wiki)
- **Issues:** [GitHub Issues](https://github.com/aceberg/fluffychat/issues)

