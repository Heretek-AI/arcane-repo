---
title: "Lobe Chat"
description: "Self-hosted Lobe Chat deployment via Docker"
---

# Lobe Chat

Self-hosted Lobe Chat deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/communication" class="tag-badge">communication</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lobe-chat/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lobe-chat/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/lobe-chat/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `lobe-chat` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `5d33e629c29e5a33a6159618973da273b3873cd37697d2fd23b928326f8a8bf7` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `lobe-chat` | docker.io/lobehub/lobe-chat:latest | Main application service |
| `lobe-chat_data` | (volume) | Persistent data storage |

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
| `LOBE_CHAT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs lobe-chat
```

**Port conflict:**
Edit `.env` and change `LOBE-CHAT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec lobe-chat ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect lobe-chat --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v lobe-chat_data:/data -v $(pwd):/backup alpine tar czf /backup/lobe-chat-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v lobe-chat_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/lobe-chat-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Lobe Chat](https://github.com/lobehub/lobe-chat)
- **Docker Image:** `docker.io/lobehub/lobe-chat:latest`
- **Documentation:** [GitHub Wiki](https://github.com/lobehub/lobe-chat/wiki)
- **Issues:** [GitHub Issues](https://github.com/lobehub/lobe-chat/issues)

