# socks5-proxy-server -- Self-Hosted Application

[socks5-proxy-server](https://github.com/nskondratev/socks5-proxy-server) is a self-hosted application available through the Awesome-Selfhosted catalog.

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
| `SOCKS5_PROXY_SERVER_PORT` | `8080` | Host port for the service |

## Services

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| `socks5-proxy-server` | `docker.io/kamuri/socks5-proxy-server:latest` | 8080 | socks5-proxy-server application |

## Managing the Service

**View logs:**

```bash
docker compose logs -f socks5-proxy-server
```

**Stop the service:**

```bash
docker compose down
```

**Update to the latest version:**

```bash
docker compose pull socks5-proxy-server
docker compose up -d
```

## Source

- Awesome-Selfhosted catalog entry: `socks5-proxy-server`
- Upstream project: https://github.com/nskondratev/socks5-proxy-server
