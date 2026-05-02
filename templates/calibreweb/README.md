# calibreweb -- Self-Hosted Application

calibreweb is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:8083](http://localhost:8083) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `CALIBREWEB_PORT` | `8083` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `calibreweb` | `docker.io/fluffybacon/calibreweb:latest` | 8083 | calibreweb application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f calibreweb
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull calibreweb
docker compose up -d
```

## Source

- Yunohost catalog entry: `calibreweb`
