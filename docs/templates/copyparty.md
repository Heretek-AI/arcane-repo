---
title: "Copyparty"
description: "Self-hosted Copyparty deployment via Docker"
---

# Copyparty

Self-hosted Copyparty deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/copyparty/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/copyparty/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/copyparty/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `copyparty` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `565f7dc58e1c055b942702cfd24f2a3a580012c71e73bb2449e4556e209f7d4a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `copyparty` | docker.io/icewhaletech/copyparty:latest | Main application service |
| `copyparty_data` | (volume) | Persistent data storage |

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
| `COPYPARTY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs copyparty
```

**Port conflict:**
Edit `.env` and change `COPYPARTY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec copyparty ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect copyparty --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v copyparty_data:/data -v $(pwd):/backup alpine tar czf /backup/copyparty-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v copyparty_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/copyparty-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Copyparty](https://github.com/icewhaletech/copyparty)
- **Docker Image:** `docker.io/icewhaletech/copyparty:latest`
- **Documentation:** [GitHub Wiki](https://github.com/icewhaletech/copyparty/wiki)
- **Issues:** [GitHub Issues](https://github.com/icewhaletech/copyparty/issues)

