# wiki-go -- Self-Hosted Application

wiki-go is a self-hosted application available through the Yunohost catalog.

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
| `WIKI_GO_PORT` | `80` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `wiki-go` | `docker.io/leomoonstudios/wiki-go:latest` | 80 | wiki-go application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f wiki-go
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull wiki-go
docker compose up -d
```

## Source

- Yunohost catalog entry: `wiki-go`
