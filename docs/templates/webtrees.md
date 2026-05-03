---
title: "Webtrees"
description: "Self-hosted Webtrees deployment via Docker"
---

# Webtrees

Self-hosted Webtrees deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/webtrees/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/webtrees/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/webtrees/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `webtrees` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7713c4187602d5da75ff22c9d19955736b20e02c462137e49de81f6a2f46d78f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `webtrees` | docker.io/dtjs48jkt/webtrees:latest | Main application service |
| `webtrees_data` | (volume) | Persistent data storage |

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
| `WEBTREES_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs webtrees
```

**Port conflict:**
Edit `.env` and change `WEBTREES_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec webtrees ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect webtrees --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v webtrees_data:/data -v $(pwd):/backup alpine tar czf /backup/webtrees-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v webtrees_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/webtrees-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Webtrees](https://github.com/dtjs48jkt/webtrees)
- **Docker Image:** `docker.io/dtjs48jkt/webtrees:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dtjs48jkt/webtrees/wiki)
- **Issues:** [GitHub Issues](https://github.com/dtjs48jkt/webtrees/issues)

