# BunkerWeb — Web Application Firewall

[BunkerWeb](https://github.com/bunkerity/bunkerweb) (10,372 ★) is an open-source, cloud-native Web Application Firewall (WAF) built on NGINX. It provides enterprise-grade security with seamless Docker, Kubernetes, Swarm, and Linux integration.

## Quick Start

1. **Configure your domain** — edit `.env` and set `BW_SERVER_NAME` to your domain.

2. **Start the firewall:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

3. **Access the web UI** at [http://localhost:7000](http://localhost:7000) (if enabled).

## Reverse Proxy Mode

To protect a backend application, enable reverse proxy mode in `.env`:

```env
BW_USE_REVERSE_PROXY=yes
BW_REVERSE_PROXY_HOST=http://app:3000
```

Then add your backend service to `docker-compose.yml`:

```yaml
app:
  image: your-app:latest
  # BunkerWeb proxies to this service
  ports:
    - "3000"
```

## Configuration

Copy `.env.example` to `.env` and edit. Key settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `BW_HTTP_PORT` | `80` | HTTP host port |
| `BW_HTTPS_PORT` | `443` | HTTPS host port |
| `BW_SERVER_NAME` | `www.example.com` | Domain name |
| `BW_AUTO_LETS_ENCRYPT` | `no` | Auto-issue SSL certificates |
| `BW_REVERSE_PROXY_HOST` | `http://app:3000` | Backend URL to protect |
| `BW_USE_MODSECURITY` | `yes` | Enable ModSecurity WAF |
| `BW_USE_ANTIBOT` | `cookie` | Antibot challenge mode |
| `BW_LIMIT_REQ_RATE` | `10r/s` | Rate limit per client |

## Security Features

- **WAF**: ModSecurity with OWASP Core Rule Set
- **SSL**: Automatic Let's Encrypt certificates
- **Antibot**: Cookie, JS challenge, CAPTCHA, reCAPTCHA
- **Threat Intel**: BunkerNet for real-time threat data
- **Rate Limiting**: Per-IP and per-URL rate controls
- **IP Filtering**: Block/country blacklists and whitelists
- **Headers**: Security headers (HSTS, CSP, X-Frame-Options)
- **Monitoring**: Real-time dashboard and Prometheus metrics

## Full Documentation

For advanced configuration (custom configurations, clustering, multi-site, API), see the [official BunkerWeb docs](https://docs.bunkerweb.io).
