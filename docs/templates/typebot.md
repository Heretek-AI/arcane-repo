---
title: "Typebot"
description: "Self-hosted Typebot deployment via Docker"
---

# Typebot

Self-hosted Typebot deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/typebot/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/typebot/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/typebot/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `typebot` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `abb692254e6578a0e97b971bdbeb57a08d5531703cee3bdad17d6af2b442539f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `typebot` | docker.io/samuellopes123/typebot:latest | Main application service |
| `typebot_data` | (volume) | Persistent data storage |

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
| `TYPEBOT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs typebot
```

**Port conflict:**
Edit `.env` and change `TYPEBOT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec typebot ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect typebot --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v typebot_data:/data -v $(pwd):/backup alpine tar czf /backup/typebot-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v typebot_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/typebot-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Typebot](https://github.com/samuellopes123/typebot)
- **Docker Image:** `docker.io/samuellopes123/typebot:latest`
- **Documentation:** [GitHub Wiki](https://github.com/samuellopes123/typebot/wiki)
- **Issues:** [GitHub Issues](https://github.com/samuellopes123/typebot/issues)

