# signaturepdf -- Self-Hosted Application

signaturepdf is a self-hosted application available through the Yunohost catalog.

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
| `SIGNATUREPDF_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `signaturepdf` | `docker.io/xgaia/signaturepdf:latest` | 8080 | signaturepdf application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f signaturepdf
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull signaturepdf
docker compose up -d
```

## Source

- Yunohost catalog entry: `signaturepdf`
