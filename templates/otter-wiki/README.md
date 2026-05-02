# Otter Wiki -- Self-Hosted Application

[Otter Wiki](https://github.com/redimp/otterwiki) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `OTTER_WIKI_PORT` | `80` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `otter-wiki` | `docker.io/redimp/otterwiki:latest` | 80 | Otter Wiki application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f otter-wiki
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull otter-wiki
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Otter Wiki`
- Upstream project: https://github.com/redimp/otterwiki
