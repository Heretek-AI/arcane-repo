# Deluge -- Self-Hosted Application

Deluge is a self-hosted application available through the Portainer catalog.

## Quick Start

1. **Copy and edit the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the application:**

   Open [http://localhost:8112](http://localhost:8112) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `DELUGE_PORT` | `8112` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `deluge` | `ghcr.io/linuxserver/deluge:latest` | 8112 | Deluge application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f deluge
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull deluge
docker compose up -d
```

## Source

- Portainer catalog entry: `Deluge`
