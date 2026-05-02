# shiori -- Self-Hosted Application

shiori is a self-hosted application available through the Yunohost catalog.

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
| `SHIORI_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `shiori` | `docker.io/radhifadlillah/shiori:latest` | 8080 | shiori application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f shiori
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull shiori
docker compose up -d
```

## Source

- Yunohost catalog entry: `shiori`
