# ctop -- Self-Hosted Application

[ctop](https://github.com/bcicen/ctop) is a self-hosted application available through the Priority catalog.

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
| `CTOP_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `ctop` | `docker.io/wrfly/ctop:latest` | 8080 | ctop application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f ctop
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull ctop
docker compose up -d
```

## Source

- Priority catalog entry: `ctop`
- Upstream project: https://github.com/bcicen/ctop
