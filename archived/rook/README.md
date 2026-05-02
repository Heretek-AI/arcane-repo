# rook -- Self-Hosted Application

[rook](https://github.com/rook/rook) is a self-hosted application available through the Priority catalog.

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
| `ROOK_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `rook` | `docker.io/rook/rook:latest` | 8080 | rook application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f rook
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull rook
docker compose up -d
```

## Source

- Priority catalog entry: `rook`
- Upstream project: https://github.com/rook/rook
