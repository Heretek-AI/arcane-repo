---
title: "Gotosocial"
description: "Self-hosted Gotosocial deployment via Docker"
---

# Gotosocial

Self-hosted Gotosocial deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/devops" class="tag-badge">devops</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gotosocial/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gotosocial/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/gotosocial/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `gotosocial` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `75963d99878d1ae22d72de93b5095c028db0ef8e00e447d36f5571703438cd69` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `gotosocial` | docker.io/superseriousbusiness/gotosocial:latest | Main application service |
| `gotosocial_data` | (volume) | Persistent data storage |

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
| `GOTOSOCIAL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs gotosocial
```

**Port conflict:**
Edit `.env` and change `GOTOSOCIAL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec gotosocial ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect gotosocial --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v gotosocial_data:/data -v $(pwd):/backup alpine tar czf /backup/gotosocial-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v gotosocial_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/gotosocial-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Gotosocial](https://github.com/superseriousbusiness/gotosocial)
- **Docker Image:** `docker.io/superseriousbusiness/gotosocial:latest`
- **Documentation:** [GitHub Wiki](https://github.com/superseriousbusiness/gotosocial/wiki)
- **Issues:** [GitHub Issues](https://github.com/superseriousbusiness/gotosocial/issues)

