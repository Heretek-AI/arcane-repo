---
title: "Dumbpad"
description: "Self-hosted Dumbpad deployment via Docker"
---

# Dumbpad

Self-hosted Dumbpad deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbpad/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbpad/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dumbpad/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dumbpad` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `239e9c9e60a518830b9cd539e31e6c52c4d5d9c04a45d6cd1cd3b799b63e96e8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `dumbpad` | docker.io/dumbwareio/dumbpad:latest | Main application service |
| `dumbpad_data` | (volume) | Persistent data storage |

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
| `DUMBPAD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs dumbpad
```

**Port conflict:**
Edit `.env` and change `DUMBPAD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec dumbpad ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect dumbpad --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v dumbpad_data:/data -v $(pwd):/backup alpine tar czf /backup/dumbpad-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v dumbpad_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/dumbpad-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Dumbpad](https://github.com/dumbwareio/dumbpad)
- **Docker Image:** `docker.io/dumbwareio/dumbpad:latest`
- **Documentation:** [GitHub Wiki](https://github.com/dumbwareio/dumbpad/wiki)
- **Issues:** [GitHub Issues](https://github.com/dumbwareio/dumbpad/issues)

