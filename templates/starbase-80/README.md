# Starbase 80 -- Self-Hosted Application

[Starbase 80](https://github.com/notclickable-jordan/starbase-80) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `STARBASE_80_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `starbase-80` | `ghcr.io/notclickable-jordan/starbase-80:latest` | 8080 | Starbase 80 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f starbase-80
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull starbase-80
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Starbase 80`
- Upstream project: https://github.com/notclickable-jordan/starbase-80
