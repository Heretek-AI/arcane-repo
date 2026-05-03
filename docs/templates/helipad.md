---
title: "Helipad"
description: "Self-hosted Helipad deployment via Docker"
---

# Helipad

Self-hosted Helipad deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/helipad/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/helipad/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/helipad/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `helipad` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `78fde278eb6d95e3d49944fc5e519b573b2d75474a620e199eb8e2767e47b797` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `helipad` | ghcr.io/ericpp/helipad:latest | Main application service |
| `helipad_data` | (volume) | Persistent data storage |

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
| `HELIPAD_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs helipad
```

**Port conflict:**
Edit `.env` and change `HELIPAD_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec helipad ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect helipad --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v helipad_data:/data -v $(pwd):/backup alpine tar czf /backup/helipad-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v helipad_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/helipad-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Helipad](https://github.com/ericpp/helipad)
- **Docker Image:** `ghcr.io/ericpp/helipad:latest`
- **Documentation:** [GitHub Wiki](https://github.com/ericpp/helipad/wiki)
- **Issues:** [GitHub Issues](https://github.com/ericpp/helipad/issues)

