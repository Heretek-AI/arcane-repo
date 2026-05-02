# Librespeed -- Self-Hosted Application

[Librespeed](https://github.com/librespeed/speedtest)) is a self-hosted application available through the Portainer catalog.

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
| `LIBRESPEED_PORT` | `80` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `librespeed` | `ghcr.io/linuxserver/librespeed:latest` | 80 | Librespeed application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f librespeed
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull librespeed
docker compose up -d
```

## Source

- Portainer catalog entry: `Librespeed`
- Upstream project: https://github.com/librespeed/speedtest)
