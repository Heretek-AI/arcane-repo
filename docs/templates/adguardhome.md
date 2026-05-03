---
title: "Adguardhome"
description: "Network-wide DNS ad blocker with parental control, safe browsing, and detailed query logging"
---

# Adguardhome

Network-wide DNS ad blocker with parental control, safe browsing, and detailed query logging

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/adguardhome/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/adguardhome/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/adguardhome/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `adguardhome` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `173468d48a81dddd91ce54c00e27bb6ab691c2d2fd9bc06bc249c07758e6b90b` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `adguardhome` | docker.io/adguard/adguardhome:latest | Main application service |
| `adguardhome_data` | (volume) | Persistent data storage |

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
| `ADGUARDHOME_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs adguardhome
```

**Port conflict:**
Edit `.env` and change `ADGUARDHOME_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec adguardhome ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect adguardhome --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v adguardhome_data:/data -v $(pwd):/backup alpine tar czf /backup/adguardhome-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v adguardhome_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/adguardhome-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Adguardhome](https://github.com/adguard/adguardhome)
- **Docker Image:** `docker.io/adguard/adguardhome:latest`
- **Documentation:** [GitHub Wiki](https://github.com/adguard/adguardhome/wiki)
- **Issues:** [GitHub Issues](https://github.com/adguard/adguardhome/issues)

