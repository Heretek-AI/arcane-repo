# elasticsearch8 -- Self-Hosted Application

elasticsearch8 is a self-hosted application available through the Yunohost catalog.

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

   Open [http://localhost:9200](http://localhost:9200) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `ELASTICSEARCH8_PORT` | `9200` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `elasticsearch8` | `docker.io/danielberteaud/elasticsearch8:latest` | 9200 | elasticsearch8 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f elasticsearch8
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull elasticsearch8
docker compose up -d
```

## Source

- Yunohost catalog entry: `elasticsearch8`
