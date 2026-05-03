---
title: "Odoo"
description: "Self-hosted Odoo deployment via Docker"
---

# Odoo

Self-hosted Odoo deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/odoo/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/odoo/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/odoo/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `odoo` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `680c16bfbe4f4706ee2522215a2ed0c1f3066a5b5e66157a912ca7c93cf2f845` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `odoo` | docker.io/bitnami/odoo:latest | Main application service |
| `odoo_data` | (volume) | Persistent data storage |

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
| `ODOO_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs odoo
```

**Port conflict:**
Edit `.env` and change `ODOO_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec odoo ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect odoo --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v odoo_data:/data -v $(pwd):/backup alpine tar czf /backup/odoo-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v odoo_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/odoo-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Odoo](https://github.com/bitnami/odoo)
- **Docker Image:** `docker.io/bitnami/odoo:latest`
- **Documentation:** [GitHub Wiki](https://github.com/bitnami/odoo/wiki)
- **Issues:** [GitHub Issues](https://github.com/bitnami/odoo/issues)

