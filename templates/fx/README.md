# fx -- Self-Hosted Application

[fx](https://github.com/rikhuijzer/fx) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `FX_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `fx` | `docker.io/rikhuijzer/fx:latest` | 8080 | fx application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f fx
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull fx
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `fx`
- Upstream project: https://github.com/rikhuijzer/fx
