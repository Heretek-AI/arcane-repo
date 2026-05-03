---
title: "Sshwifty"
description: "Self-hosted Sshwifty deployment via Docker"
---

# Sshwifty

Self-hosted Sshwifty deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sshwifty/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sshwifty/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/sshwifty/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `sshwifty` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9aaf4abbbfdc46b8b70d2f45bfce34d6d4ead1492b46e3ffa53bb7cc37a146fa` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `sshwifty` | docker.io/niruix/sshwifty:latest | Main application service |
| `sshwifty_data` | (volume) | Persistent data storage |

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
| `SSHWIFTY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs sshwifty
```

**Port conflict:**
Edit `.env` and change `SSHWIFTY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec sshwifty ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect sshwifty --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v sshwifty_data:/data -v $(pwd):/backup alpine tar czf /backup/sshwifty-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v sshwifty_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/sshwifty-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Sshwifty](https://github.com/niruix/sshwifty)
- **Docker Image:** `docker.io/niruix/sshwifty:latest`
- **Documentation:** [GitHub Wiki](https://github.com/niruix/sshwifty/wiki)
- **Issues:** [GitHub Issues](https://github.com/niruix/sshwifty/issues)

