# kata-containers -- Self-Hosted Application

[kata-containers](https://github.com/kata-containers/kata-containers) is a self-hosted application available through the Priority catalog.

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
| `KATA_CONTAINERS_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `kata-containers` | `docker.io/akoptelov/kata-containers:latest` | 8080 | kata-containers application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f kata-containers
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull kata-containers
docker compose up -d
```

## Source

- Priority catalog entry: `kata-containers`
- Upstream project: https://github.com/kata-containers/kata-containers
