---
title: "Termix"
description: "Self-hosted Termix deployment via Docker"
---

# Termix

Self-hosted Termix deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/termix/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/termix/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/termix/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `termix` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5d232c3f819126e92c24670fecd4c3b8a2bfd9c8b6764082394e3eead03145e8` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `termix` | docker.io/bugattiguy527/termix:latest | Main application service |
| `termix_data` | (volume) | Persistent data storage |

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
| `TERMIX_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs termix
```

**Port conflict:**
Edit `.env` and change `TERMIX_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec termix ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect termix --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v termix_data:/data -v $(pwd):/backup alpine tar czf /backup/termix-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v termix_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/termix-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Termix](https://github.com/bugattiguy527/termix)
- **Docker Image:** `docker.io/bugattiguy527/termix:latest`
- **Documentation:** [GitHub Wiki](https://github.com/bugattiguy527/termix/wiki)
- **Issues:** [GitHub Issues](https://github.com/bugattiguy527/termix/issues)

