# elasticsearch7 -- Self-Hosted Application

elasticsearch7 is a self-hosted application available through the Yunohost catalog.

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
| `ELASTICSEARCH7_PORT` | `9200` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `elasticsearch7` | `docker.io/egwestate/elasticsearch7:latest` | 9200 | elasticsearch7 application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f elasticsearch7
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull elasticsearch7
docker compose up -d
```

## Source

- Yunohost catalog entry: `elasticsearch7`
