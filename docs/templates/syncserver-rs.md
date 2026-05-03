---
title: "Syncserver Rs"
description: "Self-hosted Syncserver Rs deployment via Docker"
---

# Syncserver Rs

Self-hosted Syncserver Rs deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/storage" class="tag-badge">storage</a> <a href="/categories/yunohost" class="tag-badge">yunohost</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/syncserver-rs/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/syncserver-rs/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/syncserver-rs/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `syncserver-rs` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6ccad6ba6799e0c17b3f1cd3062d83884131e8efa457bcb9c0a7f7bba00d9f5e` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `syncserver-rs` | docker.io/kannasama/syncserver-rs:latest | Main application service |
| `syncserver-rs_data` | (volume) | Persistent data storage |

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
| `SYNCSERVER_RS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs syncserver-rs
```

**Port conflict:**
Edit `.env` and change `SYNCSERVER-RS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec syncserver-rs ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect syncserver-rs --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v syncserver-rs_data:/data -v $(pwd):/backup alpine tar czf /backup/syncserver-rs-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v syncserver-rs_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/syncserver-rs-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Syncserver Rs](https://github.com/kannasama/syncserver-rs)
- **Docker Image:** `docker.io/kannasama/syncserver-rs:latest`
- **Documentation:** [GitHub Wiki](https://github.com/kannasama/syncserver-rs/wiki)
- **Issues:** [GitHub Issues](https://github.com/kannasama/syncserver-rs/issues)

