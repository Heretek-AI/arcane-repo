# nodered -- Self-Hosted Application

nodered is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:1880](http://localhost:1880) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `NODERED_PORT` | `1880` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `nodered` | `docker.io/marcelocorreia/nodered:latest` | 1880 | nodered application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f nodered
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull nodered
docker compose up -d
```

## Source

- Yunohost catalog entry: `nodered`
