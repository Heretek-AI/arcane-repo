# ryot -- Self-Hosted Application

[ryot](https://github.com/IgnisDa/ryot?tab) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `RYOT_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `ryot` | `ghcr.io/ignisda/ryot:latest` | 8080 | ryot application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f ryot
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull ryot
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `ryot`
- Upstream project: https://github.com/IgnisDa/ryot?tab
