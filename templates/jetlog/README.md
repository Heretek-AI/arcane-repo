# jetlog -- Self-Hosted Application

[jetlog](https://github.com/pbogre/jetlog) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `JETLOG_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `jetlog` | `docker.io/pbogre/jetlog:latest` | 8080 | jetlog application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f jetlog
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull jetlog
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `jetlog`
- Upstream project: https://github.com/pbogre/jetlog
