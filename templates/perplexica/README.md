# perplexica -- Self-Hosted Application

perplexica is a self-hosted application available through the Umbrel catalog.

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

   Open [http://localhost:32400](http://localhost:32400) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `PERPLEXICA_PORT` | `32400` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `perplexica` | `docker.io/itzcrazykns1337/perplexica:latest` | 32400 | perplexica application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f perplexica
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull perplexica
docker compose up -d
```

## Source

- Umbrel catalog entry: `perplexica`
