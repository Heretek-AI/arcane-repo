# bookwyrm -- Self-Hosted Application

bookwyrm is a self-hosted application available through the Yunohost catalog.

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
| `BOOKWYRM_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `bookwyrm` | `ghcr.io/contrun/bookwyrm:latest` | 8080 | bookwyrm application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f bookwyrm
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull bookwyrm
docker compose up -d
```

## Source

- Yunohost catalog entry: `bookwyrm`
