# homeassistant -- Self-Hosted Application

homeassistant is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:8123](http://localhost:8123) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOMEASSISTANT_PORT` | `8123` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `homeassistant` | `ghcr.io/linuxserver/homeassistant:latest` | 8123 | homeassistant application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f homeassistant
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull homeassistant
docker compose up -d
```

## Source

- Yunohost catalog entry: `homeassistant`
