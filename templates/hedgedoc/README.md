# hedgedoc -- Self-Hosted Application

hedgedoc is a self-hosted application available through the Yunohost catalog.

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
| `HEDGEDOC_PORT` | `3000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `hedgedoc` | `ghcr.io/linuxserver/hedgedoc:latest` | 3000 | hedgedoc application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f hedgedoc
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull hedgedoc
docker compose up -d
```

## Source

- Yunohost catalog entry: `hedgedoc`
