# icecast2 -- Self-Hosted Application

icecast2 is a self-hosted application available through the Yunohost catalog.

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
| `ICECAST2_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `icecast2` | `ghcr.io/pltnk/icecast2:latest` | 8080 | icecast2 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f icecast2
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull icecast2
docker compose up -d
```

## Source

- Yunohost catalog entry: `icecast2`
