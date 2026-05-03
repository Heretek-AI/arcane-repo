---
title: "Pumperly"
description: "Self-hosted Pumperly deployment via Docker"
---

# Pumperly

Self-hosted Pumperly deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pumperly/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pumperly/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pumperly/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pumperly` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `1d332a9ee9d40895403f8cffbb7b5794c9a7a2fbd3cbfebde03a6f5b73a3d43b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `pumperly` | docker.io/drumsergio/pumperly:latest | Main application service |
| `pumperly_data` | (volume) | Persistent data storage |

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
| `PUMPERLY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs pumperly
```

**Port conflict:**
Edit `.env` and change `PUMPERLY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec pumperly ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect pumperly --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v pumperly_data:/data -v $(pwd):/backup alpine tar czf /backup/pumperly-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v pumperly_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/pumperly-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Pumperly](https://github.com/drumsergio/pumperly)
- **Docker Image:** `docker.io/drumsergio/pumperly:latest`
- **Documentation:** [GitHub Wiki](https://github.com/drumsergio/pumperly/wiki)
- **Issues:** [GitHub Issues](https://github.com/drumsergio/pumperly/issues)

