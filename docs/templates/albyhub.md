---
title: "Albyhub"
description: "Self-hosted Albyhub deployment via Docker"
---

# Albyhub

Self-hosted Albyhub deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/albyhub/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/albyhub/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/albyhub/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `albyhub` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b309450cd1e4576d3f0d675a368200343e1528002214ab5f3232adcbdb11256b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `albyhub` | docker.io/netmojo/albyhub:latest | Main application service |
| `albyhub_data` | (volume) | Persistent data storage |

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
| `ALBYHUB_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs albyhub
```

**Port conflict:**
Edit `.env` and change `ALBYHUB_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec albyhub ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect albyhub --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v albyhub_data:/data -v $(pwd):/backup alpine tar czf /backup/albyhub-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v albyhub_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/albyhub-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Albyhub](https://github.com/netmojo/albyhub)
- **Docker Image:** `docker.io/netmojo/albyhub:latest`
- **Documentation:** [GitHub Wiki](https://github.com/netmojo/albyhub/wiki)
- **Issues:** [GitHub Issues](https://github.com/netmojo/albyhub/issues)

