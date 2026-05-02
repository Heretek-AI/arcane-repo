# Flowiseai -- Self-Hosted Application

Flowiseai is a self-hosted application available through the Portainer catalog.

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
| `FLOWISEAI_PORT` | `3000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `flowiseai` | `docker.io/elestio/flowiseai:latest` | 3000 | Flowiseai application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f flowiseai
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull flowiseai
docker compose up -d
```

## Source

- Portainer catalog entry: `Flowiseai`
