# zipline -- Self-Hosted Application

zipline is a self-hosted application available through the Yunohost catalog.

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
| `ZIPLINE_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `zipline` | `docker.io/adegtyarev/zipline:latest` | 8080 | zipline application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f zipline
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull zipline
docker compose up -d
```

## Source

- Yunohost catalog entry: `zipline`
