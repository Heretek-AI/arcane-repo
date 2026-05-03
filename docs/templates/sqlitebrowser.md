---
title: "Sqlitebrowser"
description: "Self-hosted Sqlitebrowser deployment via Docker"
---

# Sqlitebrowser

Self-hosted Sqlitebrowser deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sqlitebrowser/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sqlitebrowser/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sqlitebrowser/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sqlitebrowser` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `210c39458b64bc6e6efbb5572b5771449b94562d6cd08771cf0a051d92e5f444` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `sqlitebrowser` | ghcr.io/linuxserver/sqlitebrowser:latest | Main application service |
| `sqlitebrowser_data` | (volume) | Persistent data storage |

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
| `SQLITEBROWSER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs sqlitebrowser
```

**Port conflict:**
Edit `.env` and change `SQLITEBROWSER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec sqlitebrowser ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect sqlitebrowser --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v sqlitebrowser_data:/data -v $(pwd):/backup alpine tar czf /backup/sqlitebrowser-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v sqlitebrowser_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/sqlitebrowser-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Sqlitebrowser](https://github.com/linuxserver/sqlitebrowser)
- **Docker Image:** `ghcr.io/linuxserver/sqlitebrowser:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/sqlitebrowser/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/sqlitebrowser/issues)

