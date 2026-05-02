# portainer -- Self-Hosted Application

portainer is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:9000](http://localhost:9000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORTAINER_PORT` | `9000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `portainer` | `docker.io/portainer/portainer:latest` | 9000 | portainer application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f portainer
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull portainer
docker compose up -d
```

## Source

- Umbrel catalog entry: `portainer`
