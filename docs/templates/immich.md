---
title: "Immich"
description: "Self-hosted Immich deployment via Docker"
---

# Immich

Self-hosted Immich deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/immich/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/immich/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/immich/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `immich` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4bba5525fc924fbed414ff21683aa7cda592ebe53aca8afd342665a417e09590` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `immich` | docker.io/leesonaa/immich:latest | Main application service |
| `immich_data` | (volume) | Persistent data storage |

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
| `IMMICH_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs immich
```

**Port conflict:**
Edit `.env` and change `IMMICH_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec immich ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect immich --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v immich_data:/data -v $(pwd):/backup alpine tar czf /backup/immich-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v immich_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/immich-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Immich](https://github.com/leesonaa/immich)
- **Docker Image:** `docker.io/leesonaa/immich:latest`
- **Documentation:** [GitHub Wiki](https://github.com/leesonaa/immich/wiki)
- **Issues:** [GitHub Issues](https://github.com/leesonaa/immich/issues)

