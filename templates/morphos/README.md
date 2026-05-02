# morphos -- Self-Hosted Application

morphos is a self-hosted application available through the Umbrel catalog.

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
| `MORPHOS_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `morphos` | `docker.io/wapmorgan/morphos:latest` | 8080 | morphos application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f morphos
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull morphos
docker compose up -d
```

## Source

- Umbrel catalog entry: `morphos`
