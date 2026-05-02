# pleroma -- Self-Hosted Application

pleroma is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:4000](http://localhost:4000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `PLEROMA_PORT` | `4000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `pleroma` | `docker.io/pandentia/pleroma:latest` | 4000 | pleroma application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f pleroma
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull pleroma
docker compose up -d
```

## Source

- Yunohost catalog entry: `pleroma`
