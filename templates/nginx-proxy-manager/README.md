# Nginx Proxy Manager

[Nginx Proxy Manager](https://github.com/NginxProxyManager/nginx-proxy-manager) — self-hosted via Docker Compose.

## Quick Start

1. Copy the environment file and adjust as needed:

   ```bash
   cp .env.example .env
   ```

2. Start the service:

   ```bash
   docker compose up -d
   ```

3. Access the service:

   Open [http://localhost:81](http://localhost:81) in your browser.

## Configuration

Edit `.env` to customize port and other settings. See `.env.example` for available options.

## Upstream

- [GitHub](https://github.com/NginxProxyManager/nginx-proxy-manager)
