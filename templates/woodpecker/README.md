# woodpecker -- Self-Hosted Application

woodpecker is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `WOODPECKER_PORT` | `8000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `woodpecker` | `ghcr.io/daemonless/woodpecker:latest` | 8000 | woodpecker application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f woodpecker
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull woodpecker
docker compose up -d
```

## Source

- Yunohost catalog entry: `woodpecker`
