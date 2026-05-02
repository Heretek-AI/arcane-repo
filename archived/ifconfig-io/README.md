# ifconfig-io -- Self-Hosted Application

ifconfig-io is a self-hosted application available through the Yunohost catalog.

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
| `IFCONFIG_IO_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `ifconfig-io` | `docker.io/gaoyifan/ifconfig-io:latest` | 8080 | ifconfig-io application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f ifconfig-io
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull ifconfig-io
docker compose up -d
```

## Source

- Yunohost catalog entry: `ifconfig-io`
