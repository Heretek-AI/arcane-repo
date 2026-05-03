---
title: "BunkerWeb"
description: "Open-source cloud-native Web Application Firewall (WAF) — NGINX-based with seamless Docker integration, ModSecurity, automatic Let's Encrypt certificates, and real-time security monitoring"
---

# BunkerWeb

Open-source cloud-native Web Application Firewall (WAF) — NGINX-based with seamless Docker integration, ModSecurity, automatic Let's Encrypt certificates, and real-time security monitoring

## Tags

<a href="/categories/security" class="tag-badge">security</a> <a href="/categories/proxy" class="tag-badge">proxy</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bunkerweb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bunkerweb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/bunkerweb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `bunkerweb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4906569fd103430360178f42dd0ea975fff1ac0b01a2b78346ffe5f619400cb4` |

## Quick Start

1. **Configure your domain** — edit `.env` and set `BW_SERVER_NAME` to your domain.

2. **Start the firewall:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

3. **Access the web UI** at [http://localhost:7000](http://localhost:7000) (if enabled).

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

