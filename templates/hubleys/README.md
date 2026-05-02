# Hubleys -- Self-Hosted Application

[Hubleys](https://github.com/knrdl/hubleys-dashboard) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `HUBLEYS_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `hubleys` | `ghcr.io/knrdl/hubleys-dashboard:latest` | 8080 | Hubleys application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f hubleys
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull hubleys
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Hubleys`
- Upstream project: https://github.com/knrdl/hubleys-dashboard
