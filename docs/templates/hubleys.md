---
title: "Hubleys"
description: "Self-hosted Hubleys deployment via Docker"
---

# Hubleys

Self-hosted Hubleys deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hubleys/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hubleys/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/hubleys/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `hubleys` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b5210ae51569a4fef7f8a85a3fabe68eca3acff98e520a7bc711c469fc134a66` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `hubleys` | ghcr.io/knrdl/hubleys-dashboard:latest | Main application service |
| `hubleys_data` | (volume) | Persistent data storage |

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
| `HUBLEYS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs hubleys
```

**Port conflict:**
Edit `.env` and change `HUBLEYS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec hubleys ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect hubleys --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v hubleys_data:/data -v $(pwd):/backup alpine tar czf /backup/hubleys-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v hubleys_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/hubleys-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Hubleys](https://github.com/knrdl/hubleys-dashboard)
- **Docker Image:** `ghcr.io/knrdl/hubleys-dashboard:latest`
- **Documentation:** [GitHub Wiki](https://github.com/knrdl/hubleys-dashboard/wiki)
- **Issues:** [GitHub Issues](https://github.com/knrdl/hubleys-dashboard/issues)

