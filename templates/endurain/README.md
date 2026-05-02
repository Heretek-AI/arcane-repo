# Endurain -- Self-Hosted Application

Endurain is a self-hosted application available through the Awesome-Selfhosted catalog.

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

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENDURAIN_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `endurain` | `docker.io/dk2077392/endurain:latest` | 8080 | Endurain application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f endurain
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull endurain
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Endurain`
