---
title: "Cashu Me"
description: "Self-hosted Cashu Me deployment via Docker"
---

# Cashu Me

Self-hosted Cashu Me deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cashu-me/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cashu-me/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cashu-me/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cashu-me` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9016ae45d981cfb53640bbf307ab5e817533ef68ee45cccf6809fea2079f7f54` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cashu-me` | docker.io/rstmsn/cashu-me:latest | Main application service |
| `cashu-me_data` | (volume) | Persistent data storage |

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
| `CASHU_ME_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cashu-me
```

**Port conflict:**
Edit `.env` and change `CASHU-ME_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cashu-me ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cashu-me --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cashu-me_data:/data -v $(pwd):/backup alpine tar czf /backup/cashu-me-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cashu-me_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cashu-me-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cashu Me](https://github.com/rstmsn/cashu-me)
- **Docker Image:** `docker.io/rstmsn/cashu-me:latest`
- **Documentation:** [GitHub Wiki](https://github.com/rstmsn/cashu-me/wiki)
- **Issues:** [GitHub Issues](https://github.com/rstmsn/cashu-me/issues)

