# iperf -- Self-Hosted Application

iperf is a self-hosted application available through the Portainer catalog.

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
| `IPERF_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `iperf` | `docker.io/diamanti/iperf:latest` | 8080 | iperf application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f iperf
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull iperf
docker compose up -d
```

## Source

- Portainer catalog entry: `iperf`
