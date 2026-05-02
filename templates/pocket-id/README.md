# pocket-id -- Self-Hosted Application

pocket-id is a self-hosted application available through the YunoHost catalog.

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
| `POCKET_ID_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `pocket-id` | `ghcr.io/pocket-id/pocket-id:latest` | 8080 | pocket-id application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f pocket-id
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull pocket-id
docker compose up -d
```

## Source

- YunoHost catalog entry: `pocket-id`
