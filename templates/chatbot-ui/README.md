# chatbot-ui -- Self-Hosted Application

chatbot-ui is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `CHATBOT_UI_PORT` | `3000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `chatbot-ui` | `ghcr.io/nmfretz/chatbot-ui:latest` | 3000 | chatbot-ui application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f chatbot-ui
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull chatbot-ui
docker compose up -d
```

## Source

- Umbrel catalog entry: `chatbot-ui`
