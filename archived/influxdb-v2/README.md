# influxdb_v2 -- Self-Hosted Application

influxdb_v2 is a self-hosted application available through the Yunohost catalog.

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
| `INFLUXDB_V2_PORT` | `8086` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `influxdb-v2` | `docker.io/emoneth/influxdb_v2:latest` | 8086 | influxdb_v2 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f influxdb-v2
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull influxdb-v2
docker compose up -d
```

## Source

- Yunohost catalog entry: `influxdb_v2`
