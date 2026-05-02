# Picsur -- Self-Hosted Application

[Picsur](https://github.com/CaramelFur/Picsur) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `PICSUR_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `picsur` | `ghcr.io/caramelfur/picsur:latest` | 8080 | Picsur application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f picsur
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull picsur
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Picsur`
- Upstream project: https://github.com/CaramelFur/Picsur
