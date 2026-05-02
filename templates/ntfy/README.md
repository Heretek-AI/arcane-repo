# ntfy -- Self-Hosted Application

ntfy is a self-hosted application available through the Portainer catalog.

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

   Open [http://localhost:80](http://localhost:80) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `NTFY_PORT` | `80` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `ntfy` | `docker.io/binwiederhier/ntfy:latest` | 80 | ntfy application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f ntfy
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull ntfy
docker compose up -d
```

## Source

- Portainer catalog entry: `ntfy`
