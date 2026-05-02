# Elasticsearch -- Self-Hosted Application

Elasticsearch is a self-hosted application available through the Portainer catalog.

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
| `ELASTICSEARCH_PORT` | `9200` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `elasticsearch` | `docker.io/bitnamicharts/elasticsearch:latest` | 9200 | Elasticsearch application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f elasticsearch
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull elasticsearch
docker compose up -d
```

## Source

- Portainer catalog entry: `Elasticsearch`
