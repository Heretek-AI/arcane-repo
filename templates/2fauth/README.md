# 2fauth -- Self-Hosted Application

2fauth is a self-hosted application available through the YunoHost catalog.

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
| `TWOFAUTH_PORT` | `8000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `2fauth` | `docker.io/2fauth/2fauth:latest` | 8000 | 2fauth application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f 2fauth
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull 2fauth
docker compose up -d
```

## Source

- YunoHost catalog entry: `2fauth`
