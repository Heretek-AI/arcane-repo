---
title: "Docuseal"
description: "Self-hosted Docuseal deployment via Docker"
---

# Docuseal

Self-hosted Docuseal deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docuseal/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docuseal/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docuseal/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `docuseal` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `d0031f91a277299d4677aaf0d166b7485d0317c538e6525f5ee405782140fdbb` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `docuseal` | docker.io/docuseal/docuseal:latest | Main application service |
| `docuseal_data` | (volume) | Persistent data storage |

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
| `DOCUSEAL_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs docuseal
```

**Port conflict:**
Edit `.env` and change `DOCUSEAL_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec docuseal ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect docuseal --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v docuseal_data:/data -v $(pwd):/backup alpine tar czf /backup/docuseal-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v docuseal_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/docuseal-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Docuseal](https://github.com/docuseal/docuseal)
- **Docker Image:** `docker.io/docuseal/docuseal:latest`
- **Documentation:** [GitHub Wiki](https://github.com/docuseal/docuseal/wiki)
- **Issues:** [GitHub Issues](https://github.com/docuseal/docuseal/issues)

