---
title: "Teampass"
description: "Self-hosted Teampass deployment via Docker"
---

# Teampass

Self-hosted Teampass deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/teampass/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/teampass/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/teampass/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `teampass` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `687dbe10509bf2fa0a85aeb7a858b0a33256afbe2b3dc6aca0ed25285fd7e012` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `teampass` | docker.io/teampass/teampass:latest | Main application service |
| `teampass_data` | (volume) | Persistent data storage |

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
| `TEAMPASS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs teampass
```

**Port conflict:**
Edit `.env` and change `TEAMPASS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec teampass ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect teampass --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v teampass_data:/data -v $(pwd):/backup alpine tar czf /backup/teampass-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v teampass_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/teampass-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Teampass](https://github.com/teampass/teampass)
- **Docker Image:** `docker.io/teampass/teampass:latest`
- **Documentation:** [GitHub Wiki](https://github.com/teampass/teampass/wiki)
- **Issues:** [GitHub Issues](https://github.com/teampass/teampass/issues)

