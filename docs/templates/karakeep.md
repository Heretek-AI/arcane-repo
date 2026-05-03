---
title: "Karakeep"
description: "Self-hosted Karakeep deployment via Docker"
---

# Karakeep

Self-hosted Karakeep deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/karakeep/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/karakeep/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/karakeep/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `karakeep` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `388cc326e91c05174eaaaa0416469b73992d1eed3179a0aef5431d16157145a2` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `karakeep` | docker.io/cyangze/karakeep:latest | Main application service |
| `karakeep_data` | (volume) | Persistent data storage |

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
| `KARAKEEP_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs karakeep
```

**Port conflict:**
Edit `.env` and change `KARAKEEP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec karakeep ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect karakeep --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v karakeep_data:/data -v $(pwd):/backup alpine tar czf /backup/karakeep-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v karakeep_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/karakeep-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Karakeep](https://github.com/cyangze/karakeep)
- **Docker Image:** `docker.io/cyangze/karakeep:latest`
- **Documentation:** [GitHub Wiki](https://github.com/cyangze/karakeep/wiki)
- **Issues:** [GitHub Issues](https://github.com/cyangze/karakeep/issues)

