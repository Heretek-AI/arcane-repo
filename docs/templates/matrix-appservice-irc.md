---
title: "Matrix Appservice Irc"
description: "Self-hosted Matrix Appservice Irc deployment via Docker"
---

# Matrix Appservice Irc

Self-hosted Matrix Appservice Irc deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/communication" class="tag-badge">communication</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matrix-appservice-irc/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matrix-appservice-irc/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/matrix-appservice-irc/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `matrix-appservice-irc` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3c5ae5b5df9e5b8216f500fd9fe9ca2d9f78e59a4f01670d4a7182fd65c991e1` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `matrix-appservice-irc` | docker.io/matrixdotorg/matrix-appservice-irc:latest | Main application service |
| `matrix-appservice-irc_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:8008/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8008](http://localhost:8008) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MATRIX_APPSERVICE_IRC_PORT` | `8008` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs matrix-appservice-irc
```

**Port conflict:**
Edit `.env` and change `MATRIX-APPSERVICE-IRC_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec matrix-appservice-irc ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect matrix-appservice-irc --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v matrix-appservice-irc_data:/data -v $(pwd):/backup alpine tar czf /backup/matrix-appservice-irc-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v matrix-appservice-irc_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/matrix-appservice-irc-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Matrix Appservice Irc](https://github.com/matrixdotorg/matrix-appservice-irc)
- **Docker Image:** `docker.io/matrixdotorg/matrix-appservice-irc:latest`
- **Documentation:** [GitHub Wiki](https://github.com/matrixdotorg/matrix-appservice-irc/wiki)
- **Issues:** [GitHub Issues](https://github.com/matrixdotorg/matrix-appservice-irc/issues)

