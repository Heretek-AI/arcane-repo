# Our Shopping List -- Self-Hosted Application

[Our Shopping List](https://github.com/nanawel/our-shopping-list) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `OUR_SHOPPING_LIST_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `our-shopping-list` | `docker.io/nanawel/our-shopping-list:latest` | 8080 | Our Shopping List application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f our-shopping-list
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull our-shopping-list
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `Our Shopping List`
- Upstream project: https://github.com/nanawel/our-shopping-list
