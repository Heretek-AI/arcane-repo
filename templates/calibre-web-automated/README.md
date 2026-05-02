# Calibre Web Automated -- Self-Hosted Application

[Calibre Web Automated](https://github.com/crocodilestick/Calibre-Web-Automated) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `CALIBRE_WEB_AUTOMATED_PORT` | `8083` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `calibre-web-automated` | `ghcr.io/crocodilestick/calibre-web-automated:latest` | 8083 | Calibre Web Automated application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f calibre-web-automated
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull calibre-web-automated
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Calibre Web Automated`
- Upstream project: https://github.com/crocodilestick/Calibre-Web-Automated
