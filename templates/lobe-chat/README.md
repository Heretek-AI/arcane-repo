# lobe-chat -- Self-Hosted Application

lobe-chat is a self-hosted application available through the Umbrel catalog.

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
| `LOBE_CHAT_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `lobe-chat` | `docker.io/lobehub/lobe-chat:latest` | 8080 | lobe-chat application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f lobe-chat
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull lobe-chat
docker compose up -d
```

## Source

- Umbrel catalog entry: `lobe-chat`
