---
title: "Authelia"
description: "Self-hosted Authelia deployment via Docker"
---

# Authelia

Self-hosted Authelia deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/authelia/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/authelia/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/authelia/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `authelia` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c2b5d20a76c39176dc6291115720010116726e395bf2214e030c25a9190dc422` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `authelia` | ghcr.io/authelia/authelia:latest | Main application service |
| `authelia_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:9091/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:9091](http://localhost:9091) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTHELIA_PORT` | `9091` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs authelia
```

**Port conflict:**
Edit `.env` and change `AUTHELIA_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec authelia ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect authelia --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v authelia_data:/data -v $(pwd):/backup alpine tar czf /backup/authelia-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v authelia_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/authelia-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Authelia](https://github.com/authelia/authelia)
- **Docker Image:** `ghcr.io/authelia/authelia:latest`
- **Documentation:** [GitHub Wiki](https://github.com/authelia/authelia/wiki)
- **Issues:** [GitHub Issues](https://github.com/authelia/authelia/issues)

