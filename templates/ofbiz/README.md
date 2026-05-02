# ofbiz -- Self-Hosted Application

ofbiz is a self-hosted application available through the Yunohost catalog.

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
| `OFBIZ_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `ofbiz` | `docker.io/vulhub/ofbiz:latest` | 8080 | ofbiz application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f ofbiz
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull ofbiz
docker compose up -d
```

## Source

- Yunohost catalog entry: `ofbiz`
