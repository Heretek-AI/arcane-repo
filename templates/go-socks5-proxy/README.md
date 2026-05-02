# Go-Socks5-Proxy -- Self-Hosted Application

Go-Socks5-Proxy is a self-hosted application available through the Portainer catalog.

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
| `GO_SOCKS5_PROXY_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `go-socks5-proxy` | `docker.io/serjs/go-socks5-proxy:latest` | 8080 | Go-Socks5-Proxy application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f go-socks5-proxy
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull go-socks5-proxy
docker compose up -d
```

## Source

- Portainer catalog entry: `Go-Socks5-Proxy`
