# mailman3 -- Self-Hosted Application

mailman3 is a self-hosted application available through the Yunohost catalog.

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
| `MAILMAN3_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `mailman3` | `docker.io/alexbarcelo/mailman3:latest` | 8080 | mailman3 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f mailman3
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull mailman3
docker compose up -d
```

## Source

- Yunohost catalog entry: `mailman3`
