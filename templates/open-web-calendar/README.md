# open-web-calendar -- Self-Hosted Application

open-web-calendar is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPEN_WEB_CALENDAR_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `open-web-calendar` | `docker.io/niccokunzmann/open-web-calendar:latest` | 8080 | open-web-calendar application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f open-web-calendar
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull open-web-calendar
docker compose up -d
```

## Source

- Yunohost catalog entry: `open-web-calendar`
