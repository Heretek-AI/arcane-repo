# Shifter -- Self-Hosted Application

[Shifter](https://github.com/TobySuch/Shifter) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `SHIFTER_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `shifter` | `ghcr.io/tobysuch/shifter:latest` | 8080 | Shifter application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f shifter
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull shifter
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Shifter`
- Upstream project: https://github.com/TobySuch/Shifter
