# AzuraCast -- Self-Hosted Application

[AzuraCast](https://github.com/AzuraCast/AzuraC) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `AZURACAST_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `azuracast` | `ghcr.io/azuracast/azuracast:latest` | 8080 | AzuraCast application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f azuracast
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull azuracast
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `AzuraCast`
- Upstream project: https://github.com/AzuraCast/AzuraC
