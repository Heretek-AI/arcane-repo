---
title: "Cronmaster"
description: "Self-hosted Cronmaster deployment via Docker"
---

# Cronmaster

Self-hosted Cronmaster deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/awesome-selfhosted" class="tag-badge">awesome-selfhosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cronmaster/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cronmaster/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/cronmaster/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `cronmaster` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `950c5165ecc8e38eecf245c72488a9f5bfb3ad297b0cccc44114d04866a78f8d` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `cronmaster` | ghcr.io/fccview/cronmaster:latest | Main application service |
| `cronmaster_data` | (volume) | Persistent data storage |

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
| `CRONMASTER_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs cronmaster
```

**Port conflict:**
Edit `.env` and change `CRONMASTER_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec cronmaster ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect cronmaster --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v cronmaster_data:/data -v $(pwd):/backup alpine tar czf /backup/cronmaster-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v cronmaster_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/cronmaster-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Cronmaster](https://github.com/fccview/cronmaster)
- **Docker Image:** `ghcr.io/fccview/cronmaster:latest`
- **Documentation:** [GitHub Wiki](https://github.com/fccview/cronmaster/wiki)
- **Issues:** [GitHub Issues](https://github.com/fccview/cronmaster/issues)

