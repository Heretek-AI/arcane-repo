# chyrplite -- Self-Hosted Application

chyrplite is a self-hosted application available through the Yunohost catalog.

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
| `CHYRPLITE_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `chyrplite` | `docker.io/tbelbek/chyrplite:latest` | 8080 | chyrplite application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f chyrplite
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull chyrplite
docker compose up -d
```

## Source

- Yunohost catalog entry: `chyrplite`
