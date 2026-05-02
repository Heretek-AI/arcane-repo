# Actual -- Self-Hosted Application

Actual is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:5006](http://localhost:5006) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `ACTUAL_PORT` | `5006` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `actual` | `docker.io/phoenixashes/actual:latest` | 5006 | Actual application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f actual
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull actual
docker compose up -d
```

## Source

- Portainer catalog entry: `Actual`
