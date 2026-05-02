# domain-locker -- Self-Hosted Application

domain-locker is a self-hosted application available through the Umbrel catalog.

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
| `DOMAIN_LOCKER_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `domain-locker` | `ghcr.io/lissy93/domain-locker:latest` | 8080 | domain-locker application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f domain-locker
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull domain-locker
docker compose up -d
```

## Source

- Umbrel catalog entry: `domain-locker`
