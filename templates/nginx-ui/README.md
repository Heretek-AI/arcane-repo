# Nginx UI

[Nginx UI](https://github.com/0xJacky/nginx-ui) (11,100★) — Yet another WebUI for Nginx. Modern dashboard for managing Nginx configurations, sites, SSL certificates, and logs. Replaces the host's Nginx with a containerized instance managed through a rich web interface.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` to customize ports:**

   ```ini
   NGINX_UI_HTTP_PORT=8080
   NGINX_UI_HTTPS_PORT=8443
   ```

3. **Start the service:**

   ```bash
   docker compose up -d
   ```

4. **Complete initial setup:**

   Open [http://localhost:8080/install](http://localhost:8080/install) in your browser to configure admin credentials and Nginx paths.

## Configuration

Copy `.env.example` to `.env` and edit as needed.

| Variable | Default | Description |
|---|---|---|
| `NGINX_UI_HTTP_PORT` | `8080` | Host port for HTTP/Nginx UI dashboard |
| `NGINX_UI_HTTPS_PORT` | `8443` | Host port for HTTPS |
| `TZ` | `UTC` | Container timezone |
| `NGINX_WEBROOT` | `./www` | Local directory for static website files |

## Service Details

- **Web UI Dashboard** — Full management of Nginx sites, upstreams, SSL certs (Let's Encrypt auto-renewal), and configuration editing on port 8080
- **Nginx Instance** — Containerized Nginx serving traffic on ports 80 (HTTP) and 443 (HTTPS)
- **ChatGPT Assistant** — Built-in AI assistant for configuration help
- **Web Terminal** — In-browser terminal for server management
- **NgxConfigEditor** — Block-based Nginx configuration editor with syntax highlighting

### Important Notes

1. When using this container for the first time, ensure the volume mapped to `/etc/nginx` is **empty**.
2. On first run, visit `http://localhost:8080/install` to complete setup.
3. Default login after setup: `admin` / `admin` (change immediately).
4. For Debian-style configurations, Nginx UI follows the `sites-available` / `sites-enabled` pattern.

## Upstream

- [GitHub Repository](https://github.com/0xJacky/nginx-ui)
- [Documentation](https://nginxui.com)
- [Docker Hub Image](https://hub.docker.com/r/uozi/nginx-ui)
