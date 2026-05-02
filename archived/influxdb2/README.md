# influxdb2 -- Self-Hosted Application

influxdb2 is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:8086](http://localhost:8086) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `INFLUXDB2_PORT` | `8086` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `influxdb2` | `docker.io/samerlabban/influxdb2:latest` | 8086 | influxdb2 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f influxdb2
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull influxdb2
docker compose up -d
```

## Source

- Umbrel catalog entry: `influxdb2`
