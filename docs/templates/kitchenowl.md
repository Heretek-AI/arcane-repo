---
title: "Kitchenowl"
description: "Self-hosted Kitchenowl deployment via Docker"
---

# Kitchenowl

Self-hosted Kitchenowl deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kitchenowl/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kitchenowl/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/kitchenowl/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `kitchenowl` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `290852920fe4f8d46df904c8e6302a5926d426a9c81d402d08f22ac3c816c414` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `kitchenowl` | docker.io/tombursch/kitchenowl:latest | Main application service |
| `kitchenowl_data` | (volume) | Persistent data storage |

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
| `KITCHENOWL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs kitchenowl
```

**Port conflict:**
Edit `.env` and change `KITCHENOWL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec kitchenowl ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect kitchenowl --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v kitchenowl_data:/data -v $(pwd):/backup alpine tar czf /backup/kitchenowl-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v kitchenowl_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/kitchenowl-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Kitchenowl](https://github.com/tombursch/kitchenowl)
- **Docker Image:** `docker.io/tombursch/kitchenowl:latest`
- **Documentation:** [GitHub Wiki](https://github.com/tombursch/kitchenowl/wiki)
- **Issues:** [GitHub Issues](https://github.com/tombursch/kitchenowl/issues)

