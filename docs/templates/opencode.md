---
title: "Opencode"
description: "Self-hosted Opencode deployment via Docker"
---

# Opencode

Self-hosted Opencode deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opencode/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opencode/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/opencode/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `opencode` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `36cb0376980dca1c669b8af19b210c1aca6d37bf2ae579f85b49cfeb6d0bd486` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `opencode` | docker.io/smanx/opencode:latest | Main application service |
| `opencode_data` | (volume) | Persistent data storage |

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
| `OPENCODE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs opencode
```

**Port conflict:**
Edit `.env` and change `OPENCODE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec opencode ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect opencode --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v opencode_data:/data -v $(pwd):/backup alpine tar czf /backup/opencode-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v opencode_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/opencode-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Opencode](https://github.com/smanx/opencode)
- **Docker Image:** `docker.io/smanx/opencode:latest`
- **Documentation:** [GitHub Wiki](https://github.com/smanx/opencode/wiki)
- **Issues:** [GitHub Issues](https://github.com/smanx/opencode/issues)

