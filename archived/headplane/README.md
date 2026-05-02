# headplane -- Self-Hosted Application

headplane is a self-hosted application available through the Yunohost catalog.

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
| `HEADPLANE_PORT` | `8000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `headplane` | `docker.io/tkaxv7s/headplane:latest` | 8000 | headplane application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f headplane
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull headplane
docker compose up -d
```

## Source

- Yunohost catalog entry: `headplane`
