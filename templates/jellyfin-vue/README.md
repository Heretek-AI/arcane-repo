# jellyfin-vue -- Self-Hosted Application

jellyfin-vue is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:8096](http://localhost:8096) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `JELLYFIN_VUE_PORT` | `8096` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `jellyfin-vue` | `ghcr.io/jellyfin/jellyfin-vue:latest` | 8096 | jellyfin-vue application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f jellyfin-vue
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull jellyfin-vue
docker compose up -d
```

## Source

- Yunohost catalog entry: `jellyfin-vue`
