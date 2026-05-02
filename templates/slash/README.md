# Slash -- Self-Hosted Application

[Slash](https://github.com/yourselfhosted/slash) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `SLASH_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `slash` | `docker.io/yourselfhosted/slash:latest` | 8080 | Slash application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f slash
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull slash
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Slash`
- Upstream project: https://github.com/yourselfhosted/slash
