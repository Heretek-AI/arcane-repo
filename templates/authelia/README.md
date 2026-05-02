# Authelia -- Self-Hosted Application

Authelia is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:9091](http://localhost:9091) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTHELIA_PORT` | `9091` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `authelia` | `ghcr.io/authelia/authelia:latest` | 9091 | Authelia application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f authelia
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull authelia
docker compose up -d
```

## Source

- Portainer catalog entry: `Authelia`
