---
title: "Passbolt"
description: "Self-hosted Passbolt deployment via Docker"
---

# Passbolt

Self-hosted Passbolt deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/passbolt/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/passbolt/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/passbolt/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `passbolt` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9650d7455752da90a1a840d792d56661537500483f442bf2223e8263a2c09a49` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `passbolt` | docker.io/passbolt/passbolt:latest | Main application service |
| `passbolt_data` | (volume) | Persistent data storage |

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
| `PASSBOLT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs passbolt
```

**Port conflict:**
Edit `.env` and change `PASSBOLT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec passbolt ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect passbolt --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v passbolt_data:/data -v $(pwd):/backup alpine tar czf /backup/passbolt-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v passbolt_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/passbolt-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Passbolt](https://github.com/passbolt/passbolt)
- **Docker Image:** `docker.io/passbolt/passbolt:latest`
- **Documentation:** [GitHub Wiki](https://github.com/passbolt/passbolt/wiki)
- **Issues:** [GitHub Issues](https://github.com/passbolt/passbolt/issues)

