---
title: "Flowiseai"
description: "Self-hosted Flowiseai deployment via Docker"
---

# Flowiseai

Self-hosted Flowiseai deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flowiseai/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flowiseai/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/flowiseai/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `flowiseai` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `15caf659728450b3ead340784ce4a8341aa3801778a4e3338500807eb17cebf2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `flowiseai` | docker.io/elestio/flowiseai:latest | Main application service |
| `flowiseai_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:3000/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `FLOWISEAI_PORT` | `3000` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs flowiseai
```

**Port conflict:**
Edit `.env` and change `FLOWISEAI_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec flowiseai ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect flowiseai --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v flowiseai_data:/data -v $(pwd):/backup alpine tar czf /backup/flowiseai-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v flowiseai_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/flowiseai-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Flowiseai](https://github.com/elestio/flowiseai)
- **Docker Image:** `docker.io/elestio/flowiseai:latest`
- **Documentation:** [GitHub Wiki](https://github.com/elestio/flowiseai/wiki)
- **Issues:** [GitHub Issues](https://github.com/elestio/flowiseai/issues)

