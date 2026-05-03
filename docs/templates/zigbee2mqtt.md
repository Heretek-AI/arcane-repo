---
title: "Zigbee2Mqtt"
description: "Self-hosted Zigbee2Mqtt deployment via Docker"
---

# Zigbee2Mqtt

Self-hosted Zigbee2Mqtt deployment via Docker

## Tags

<a href="/categories/self-hosted" class="tag-badge">self-hosted</a> <a href="/categories/umbrel" class="tag-badge">umbrel</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/zigbee2mqtt/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/zigbee2mqtt/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/zigbee2mqtt/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `zigbee2mqtt` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `2ff468f067dfc5570e1f2facd7448422e6e733edca692d2b76843854e71572c5` |

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `zigbee2mqtt` | ghcr.io/koenkk/zigbee2mqtt:latest | Main application service |
| `zigbee2mqtt_data` | (volume) | Persistent data storage |

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
| `ZIGBEE2MQTT_PORT` | `8080` | Configuration variable |

## Troubleshooting

**Container won't start:**
```bash
docker compose logs zigbee2mqtt
```

**Port conflict:**
Edit `.env` and change `ZIGBEE2MQTT_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec zigbee2mqtt ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect zigbee2mqtt --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v zigbee2mqtt_data:/data -v $(pwd):/backup alpine tar czf /backup/zigbee2mqtt-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v zigbee2mqtt_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/zigbee2mqtt-backup.tar.gz -C /"
docker compose up -d
```

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage

## Links

- **Project Homepage:** [Zigbee2Mqtt](https://github.com/koenkk/zigbee2mqtt)
- **Docker Image:** `ghcr.io/koenkk/zigbee2mqtt:latest`
- **Documentation:** [GitHub Wiki](https://github.com/koenkk/zigbee2mqtt/wiki)
- **Issues:** [GitHub Issues](https://github.com/koenkk/zigbee2mqtt/issues)

