---
title: "Openbudgeteer"
description: "Self-hosted Openbudgeteer deployment via Docker"
---

# Openbudgeteer

Self-hosted Openbudgeteer deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openbudgeteer/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openbudgeteer/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openbudgeteer/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openbudgeteer` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `966c9b6785593dbcae07a3f6baaa479f6c4f7a78dac6bf363aa42090e634a711` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `openbudgeteer` | docker.io/axelander/openbudgeteer:latest | Main application service |
| `openbudgeteer_data` | (volume) | Persistent data storage |

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
| `OPENBUDGETEER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs openbudgeteer
```

**Port conflict:**
Edit `.env` and change `OPENBUDGETEER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec openbudgeteer ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect openbudgeteer --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v openbudgeteer_data:/data -v $(pwd):/backup alpine tar czf /backup/openbudgeteer-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v openbudgeteer_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/openbudgeteer-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Openbudgeteer](https://github.com/axelander/openbudgeteer)
- **Docker Image:** `docker.io/axelander/openbudgeteer:latest`
- **Documentation:** [GitHub Wiki](https://github.com/axelander/openbudgeteer/wiki)
- **Issues:** [GitHub Issues](https://github.com/axelander/openbudgeteer/issues)

