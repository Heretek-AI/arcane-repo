# gitea-mirror -- Self-Hosted Application

gitea-mirror is a self-hosted application available through the Umbrel catalog.

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
| `GITEA_MIRROR_PORT` | `3000` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `gitea-mirror` | `docker.io/ckevi/gitea-mirror:latest` | 3000 | gitea-mirror application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f gitea-mirror
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull gitea-mirror
docker compose up -d
```

## Source

- Umbrel catalog entry: `gitea-mirror`
