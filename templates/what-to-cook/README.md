# What To Cook? -- Self-Hosted Application

[What To Cook?](https://github.com/kassner/whattocook) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `WHAT_TO_COOK_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `what-to-cook` | `ghcr.io/kassner/whattocook:latest` | 8080 | What To Cook? application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f what-to-cook
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull what-to-cook
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `What To Cook?`
- Upstream project: https://github.com/kassner/whattocook
