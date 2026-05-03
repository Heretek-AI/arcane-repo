---
title: "Rustdesk Server"
description: "Self-hosted Rustdesk Server deployment via Docker"
---

# Rustdesk Server

Self-hosted Rustdesk Server deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rustdesk-server/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rustdesk-server/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/rustdesk-server/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `rustdesk-server` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ad4af7d654f8ceb1b355ff41ce1552bd7ab2b03efe67feb26fe6997915a8b1c8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `rustdesk-server` | ghcr.io/rustdesk/rustdesk-server:latest | Main application service |
| `rustdesk-server_data` | (volume) | Persistent data storage |

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
| `RUSTDESK_SERVER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs rustdesk-server
```

**Port conflict:**
Edit `.env` and change `RUSTDESK-SERVER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec rustdesk-server ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect rustdesk-server --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v rustdesk-server_data:/data -v $(pwd):/backup alpine tar czf /backup/rustdesk-server-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v rustdesk-server_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/rustdesk-server-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Rustdesk Server](https://github.com/rustdesk/rustdesk-server)
- **Docker Image:** `ghcr.io/rustdesk/rustdesk-server:latest`
- **Documentation:** [GitHub Wiki](https://github.com/rustdesk/rustdesk-server/wiki)
- **Issues:** [GitHub Issues](https://github.com/rustdesk/rustdesk-server/issues)

