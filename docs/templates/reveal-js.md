---
title: "Reveal.Js"
description: "Self-hosted Reveal.Js deployment via Docker"
---

# Reveal.Js

Self-hosted Reveal.Js deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/portainer" class="tag-badge">portainer</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/reveal-js/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/reveal-js/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/reveal-js/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `reveal-js` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `fd6387625686c6e2e4e5e09f128e916202d82218c417ad02dc73ecd46b6b8fe0` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `reveal-js` | ghcr.io/cloudogu/reveal.js:latest | Main application service |
| `reveal-js_data` | (volume) | Persistent data storage |

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
| `REVEAL_JS_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs reveal-js
```

**Port conflict:**
Edit `.env` and change `REVEAL-JS_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec reveal-js ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect reveal-js --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v reveal-js_data:/data -v $(pwd):/backup alpine tar czf /backup/reveal-js-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v reveal-js_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/reveal-js-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Reveal.Js](https://github.com/cloudogu/reveal.js)
- **Docker Image:** `ghcr.io/cloudogu/reveal.js:latest`
- **Documentation:** [GitHub Wiki](https://github.com/cloudogu/reveal.js/wiki)
- **Issues:** [GitHub Issues](https://github.com/cloudogu/reveal.js/issues)

