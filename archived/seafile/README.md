# seafile -- Self-Hosted Application

seafile is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:80](http://localhost:80) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `SEAFILE_PORT` | `80` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `seafile` | `docker.io/jenserat/seafile:latest` | 80 | seafile application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f seafile
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull seafile
docker compose up -d
```

## Source

- Umbrel catalog entry: `seafile`
