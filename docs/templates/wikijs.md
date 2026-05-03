---
title: "Wikijs"
description: "Self-hosted Wikijs deployment via Docker"
---

# Wikijs

Self-hosted Wikijs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/cms" class="tag-badge">cms</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikijs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikijs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/wikijs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `wikijs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `814fe3c9270bd62e6a8022ff14df52c065351b26f3088e572f04fdec583b307a` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `wikijs` | ghcr.io/linuxserver/wikijs:latest | Main application service |
| `wikijs_data` | (volume) | Persistent data storage |

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
   curl -s http://localhost:80/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:80](http://localhost:80) in your browser.

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WIKIJS_PORT` | `80` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs wikijs
```

**Port conflict:**
Edit `.env` and change `WIKIJS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec wikijs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect wikijs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v wikijs_data:/data -v $(pwd):/backup alpine tar czf /backup/wikijs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v wikijs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/wikijs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Wikijs](https://github.com/linuxserver/wikijs)
- **Docker Image:** `ghcr.io/linuxserver/wikijs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/linuxserver/wikijs/wiki)
- **Issues:** [GitHub Issues](https://github.com/linuxserver/wikijs/issues)

