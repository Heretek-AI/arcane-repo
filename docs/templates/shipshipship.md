---
title: "Shipshipship"
description: "Self-hosted Shipshipship deployment via Docker"
---

# Shipshipship

Self-hosted Shipshipship deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shipshipship/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shipshipship/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shipshipship/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `shipshipship` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `fd7752adcaa1e8a16374b6dc1bc059e866e2d7bf71a6cf9a604c6bf6656c9b80` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `shipshipship` | docker.io/nelkinsky/shipshipship:latest | Main application service |
| `shipshipship_data` | (volume) | Persistent data storage |

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
| `SHIPSHIPSHIP_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs shipshipship
```

**Port conflict:**
Edit `.env` and change `SHIPSHIPSHIP_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec shipshipship ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect shipshipship --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v shipshipship_data:/data -v $(pwd):/backup alpine tar czf /backup/shipshipship-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v shipshipship_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/shipshipship-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Shipshipship](https://github.com/nelkinsky/shipshipship)
- **Docker Image:** `docker.io/nelkinsky/shipshipship:latest`
- **Documentation:** [GitHub Wiki](https://github.com/nelkinsky/shipshipship/wiki)
- **Issues:** [GitHub Issues](https://github.com/nelkinsky/shipshipship/issues)

