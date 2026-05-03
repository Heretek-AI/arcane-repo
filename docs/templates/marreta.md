---
title: "Marreta"
description: "Self-hosted Marreta deployment via Docker"
---

# Marreta

Self-hosted Marreta deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/marreta/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/marreta/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/marreta/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `marreta` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `41f934ad3b5b62763d8825313137c28e97a98f4555c63f621509a5eb61d83e77` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `marreta` | ghcr.io/manualdousuario/marreta:latest | Main application service |
| `marreta_data` | (volume) | Persistent data storage |

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
| `MARRETA_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs marreta
```

**Port conflict:**
Edit `.env` and change `MARRETA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec marreta ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect marreta --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v marreta_data:/data -v $(pwd):/backup alpine tar czf /backup/marreta-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v marreta_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/marreta-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Marreta](https://github.com/manualdousuario/marreta)
- **Docker Image:** `ghcr.io/manualdousuario/marreta:latest`
- **Documentation:** [GitHub Wiki](https://github.com/manualdousuario/marreta/wiki)
- **Issues:** [GitHub Issues](https://github.com/manualdousuario/marreta/issues)

