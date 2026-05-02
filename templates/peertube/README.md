# peertube -- Self-Hosted Application

peertube is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:9000](http://localhost:9000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `PEERTUBE_PORT` | `9000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `peertube` | `docker.io/chocobozzz/peertube:latest` | 9000 | peertube application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f peertube
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull peertube
docker compose up -d
```

## Source

- Yunohost catalog entry: `peertube`
