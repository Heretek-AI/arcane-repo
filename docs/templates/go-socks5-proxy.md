---
title: "Go Socks5 Proxy"
description: "Self-hosted Go Socks5 Proxy deployment via Docker"
---

# Go Socks5 Proxy

Self-hosted Go Socks5 Proxy deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/go-socks5-proxy/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/go-socks5-proxy/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/go-socks5-proxy/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `go-socks5-proxy` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `67d69c3502d90e42592db8e02b4a84ff594f4836f9a08fdfdeb4b834194cea46` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `go-socks5-proxy` | docker.io/serjs/go-socks5-proxy:latest | Main application service |
| `go-socks5-proxy_data` | (volume) | Persistent data storage |

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
| `GO_SOCKS5_PROXY_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs go-socks5-proxy
```

**Port conflict:**
Edit `.env` and change `GO-SOCKS5-PROXY_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec go-socks5-proxy ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect go-socks5-proxy --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v go-socks5-proxy_data:/data -v $(pwd):/backup alpine tar czf /backup/go-socks5-proxy-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v go-socks5-proxy_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/go-socks5-proxy-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Go Socks5 Proxy](https://github.com/serjs/go-socks5-proxy)
- **Docker Image:** `docker.io/serjs/go-socks5-proxy:latest`
- **Documentation:** [GitHub Wiki](https://github.com/serjs/go-socks5-proxy/wiki)
- **Issues:** [GitHub Issues](https://github.com/serjs/go-socks5-proxy/issues)

