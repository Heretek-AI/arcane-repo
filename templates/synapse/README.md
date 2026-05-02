# synapse -- Self-Hosted Application

synapse is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:8008](http://localhost:8008) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNAPSE_PORT` | `8008` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `synapse` | `docker.io/matrixdotorg/synapse:latest` | 8008 | synapse application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f synapse
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull synapse
docker compose up -d
```

## Source

- Umbrel catalog entry: `synapse`
