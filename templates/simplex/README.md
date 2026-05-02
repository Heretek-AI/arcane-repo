# simplex -- Self-Hosted Application

simplex is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:32400](http://localhost:32400) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `SIMPLEX_PORT` | `32400` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `simplex` | `docker.io/chetanketh/simplex:latest` | 32400 | simplex application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f simplex
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull simplex
docker compose up -d
```

## Source

- Yunohost catalog entry: `simplex`
