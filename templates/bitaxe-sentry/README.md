# bitaxe-sentry -- Self-Hosted Application

bitaxe-sentry is a self-hosted application available through the Umbrel catalog.

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
| `BITAXE_SENTRY_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `bitaxe-sentry` | `docker.io/zachprice105/bitaxe-sentry:latest` | 8080 | bitaxe-sentry application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f bitaxe-sentry
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull bitaxe-sentry
docker compose up -d
```

## Source

- Umbrel catalog entry: `bitaxe-sentry`
