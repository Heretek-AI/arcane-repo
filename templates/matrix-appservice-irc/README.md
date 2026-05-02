# matrix-appservice-irc -- Self-Hosted Application

matrix-appservice-irc is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:8008](http://localhost:8008) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `MATRIX_APPSERVICE_IRC_PORT` | `8008` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `matrix-appservice-irc` | `docker.io/matrixdotorg/matrix-appservice-irc:latest` | 8008 | matrix-appservice-irc application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f matrix-appservice-irc
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull matrix-appservice-irc
docker compose up -d
```

## Source

- Yunohost catalog entry: `matrix-appservice-irc`
