# YunoHost -- Self-Hosted Application

[YunoHost](https://github.com/YunoHost/yunohost) is a self-hosted application available through the Priority catalog.

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
| `YUNOHOST_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `yunohost` | `docker.io/domainelibre/yunohost:latest` | 8080 | YunoHost application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f yunohost
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull yunohost
docker compose up -d
```

## Source

- Priority catalog entry: `YunoHost`
- Upstream project: https://github.com/YunoHost/yunohost
