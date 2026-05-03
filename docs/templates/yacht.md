---
title: "Yacht"
description: "Self-hosted Yacht deployment via Docker"
---

# Yacht

Self-hosted Yacht deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yacht/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yacht/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/yacht/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `yacht` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `93d7c0a29346ea2c9f6d7b5cc405c34c469e2dbfe4b4be1aa27c26346902e4ee` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `yacht` | ghcr.io/selfhostedpro/yacht:latest | Main application service |
| `yacht_data` | (volume) | Persistent data storage |

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
| `YACHT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs yacht
```

**Port conflict:**
Edit `.env` and change `YACHT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec yacht ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect yacht --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v yacht_data:/data -v $(pwd):/backup alpine tar czf /backup/yacht-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v yacht_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/yacht-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Yacht](https://github.com/selfhostedpro/yacht)
- **Docker Image:** `ghcr.io/selfhostedpro/yacht:latest`
- **Documentation:** [GitHub Wiki](https://github.com/selfhostedpro/yacht/wiki)
- **Issues:** [GitHub Issues](https://github.com/selfhostedpro/yacht/issues)

