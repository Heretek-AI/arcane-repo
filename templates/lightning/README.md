# lightning -- Self-Hosted Application

lightning is a self-hosted application available through the Umbrel catalog.

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
| `LIGHTNING_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `lightning` | `docker.io/btcpayserver/lightning:latest` | 8080 | lightning application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f lightning
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull lightning
docker compose up -d
```

## Source

- Umbrel catalog entry: `lightning`
