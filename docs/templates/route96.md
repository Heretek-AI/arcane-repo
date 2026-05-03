---
title: "Route96"
description: "Self-hosted Route96 deployment via Docker"
---

# Route96

Self-hosted Route96 deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/route96/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/route96/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/route96/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `route96` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `39dc09ecf12c580249750e2a761197337fa652ffa8c94ec66d86b0b084b5dd92` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `route96` | docker.io/voidic/route96:latest | Main application service |
| `route96_data` | (volume) | Persistent data storage |

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
| `ROUTE96_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs route96
```

**Port conflict:**
Edit `.env` and change `ROUTE96_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec route96 ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect route96 --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v route96_data:/data -v $(pwd):/backup alpine tar czf /backup/route96-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v route96_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/route96-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Route96](https://github.com/voidic/route96)
- **Docker Image:** `docker.io/voidic/route96:latest`
- **Documentation:** [GitHub Wiki](https://github.com/voidic/route96/wiki)
- **Issues:** [GitHub Issues](https://github.com/voidic/route96/issues)

