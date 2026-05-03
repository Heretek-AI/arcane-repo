---
title: "Moodle"
description: "Self-hosted Moodle deployment via Docker"
---

# Moodle

Self-hosted Moodle deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/moodle/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/moodle/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/moodle/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `moodle` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `7553434affa3232cf752936e9c1008e514f6d7d0fe1d84e85c5fe1ab6625be07` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `moodle` | docker.io/bitnami/moodle:latest | Main application service |
| `moodle_data` | (volume) | Persistent data storage |

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
| `MOODLE_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs moodle
```

**Port conflict:**
Edit `.env` and change `MOODLE_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec moodle ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect moodle --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v moodle_data:/data -v $(pwd):/backup alpine tar czf /backup/moodle-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v moodle_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/moodle-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Moodle](https://github.com/bitnami/moodle)
- **Docker Image:** `docker.io/bitnami/moodle:latest`
- **Documentation:** [GitHub Wiki](https://github.com/bitnami/moodle/wiki)
- **Issues:** [GitHub Issues](https://github.com/bitnami/moodle/issues)

