# synapse-admin -- Self-Hosted Application

synapse-admin is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:8008](http://localhost:8008) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `SYNAPSE_ADMIN_PORT` | `8008` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `synapse-admin` | `docker.io/awesometechnologies/synapse-admin:latest` | 8008 | synapse-admin application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f synapse-admin
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull synapse-admin
docker compose up -d
```

## Source

- Yunohost catalog entry: `synapse-admin`
