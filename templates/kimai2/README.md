# kimai2 -- Self-Hosted Application

kimai2 is a self-hosted application available through the Yunohost catalog.

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
| `KIMAI2_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `kimai2` | `docker.io/kimai/kimai2:latest` | 8080 | kimai2 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f kimai2
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull kimai2
docker compose up -d
```

## Source

- Yunohost catalog entry: `kimai2`
