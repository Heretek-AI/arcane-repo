---
title: "Cashpilot"
description: "Self-hosted Cashpilot deployment via Docker"
---

# Cashpilot

Self-hosted Cashpilot deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cashpilot/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cashpilot/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cashpilot/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cashpilot` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6b3feb7fe885cf61b631de251b842dd3a250c3a0d0a7118f45e54e04e6388311` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cashpilot` | docker.io/drumsergio/cashpilot:latest | Main application service |
| `cashpilot_data` | (volume) | Persistent data storage |

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
| `CASHPILOT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cashpilot
```

**Port conflict:**
Edit `.env` and change `CASHPILOT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cashpilot ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cashpilot --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cashpilot_data:/data -v $(pwd):/backup alpine tar czf /backup/cashpilot-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cashpilot_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cashpilot-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cashpilot](https://github.com/drumsergio/cashpilot)
- **Docker Image:** `docker.io/drumsergio/cashpilot:latest`
- **Documentation:** [GitHub Wiki](https://github.com/drumsergio/cashpilot/wiki)
- **Issues:** [GitHub Issues](https://github.com/drumsergio/cashpilot/issues)

