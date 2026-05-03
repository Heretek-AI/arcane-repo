---
title: "Agora"
description: "Self-hosted Agora deployment via Docker"
---

# Agora

Self-hosted Agora deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agora/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agora/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/agora/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `agora` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `0c09403c459d1fe9fef3363118ab87dc1de7240916a904f686e0bd180be9bb4f` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `agora` | docker.io/broadinstitute/agora:latest | Main application service |
| `agora_data` | (volume) | Persistent data storage |

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
| `AGORA_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs agora
```

**Port conflict:**
Edit `.env` and change `AGORA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec agora ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect agora --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v agora_data:/data -v $(pwd):/backup alpine tar czf /backup/agora-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v agora_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/agora-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Agora](https://github.com/broadinstitute/agora)
- **Docker Image:** `docker.io/broadinstitute/agora:latest`
- **Documentation:** [GitHub Wiki](https://github.com/broadinstitute/agora/wiki)
- **Issues:** [GitHub Issues](https://github.com/broadinstitute/agora/issues)

