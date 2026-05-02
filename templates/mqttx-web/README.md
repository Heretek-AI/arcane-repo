# mqttx-web -- Self-Hosted Application

mqttx-web is a self-hosted application available through the Umbrel catalog.

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
| `MQTTX_WEB_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `mqttx-web` | `docker.io/emqx/mqttx-web:latest` | 8080 | mqttx-web application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f mqttx-web
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull mqttx-web
docker compose up -d
```

## Source

- Umbrel catalog entry: `mqttx-web`
