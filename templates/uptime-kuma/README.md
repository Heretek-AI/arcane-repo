# Uptime Kuma

Self-hosted monitoring tool for tracking uptime of websites, APIs, databases, and services with alerting. Uptime Kuma provides a clean dashboard, multi-protocol monitoring (HTTP, TCP, DNS, Docker, and more), and notifications via 90+ integrations including Slack, Discord, Telegram, email, and PagerDuty.

---

## Project Overview

**What it does:** Uptime Kuma monitors your services and reports their availability in real time. It supports HTTP(S), TCP, DNS, Docker container health, keyword matching, and more. When a service goes down, it sends alerts through your preferred notification channel.

**Who it's for:** Anyone running self-hosted services who needs a simple, reliable uptime monitor without relying on third-party SaaS monitoring tools. Ideal for homelab operators, small teams, and developers managing their own infrastructure.

**Key features:**

- Monitor HTTP(S), TCP, Ping, DNS, Docker, Steam Game Server, and more
- 90+ notification integrations (Slack, Discord, Telegram, email, PagerDuty, etc.)
- Beautiful, responsive status page with public sharing support
- Certificate monitoring with expiry alerts
- Multi-language support (30+ languages)
- Lightweight — single container, SQLite database, minimal resource usage

---

## Architecture

| Component | Details |
|---|---|
| **Image** | `ghcr.io/louislam/uptime-kuma:latest` |
| **Port** | `3001` (web UI, configurable via `UPTIME_KUMA_PORT`) |
| **Volume** | `uptime-kuma_data` mounted at `/data` — stores the SQLite database, configuration, and backups |
| **Health check** | HTTP probe to `http://localhost:3001/` every 30s with a 30s startup grace period |
| **Restart policy** | `unless-stopped` |

This is a single-container deployment. All data persists in the `uptime-kuma_data` named volume. No external database or cache is required.

---

## Quick Start

1. **Clone or download the template directory.**

2. **Create your environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Start the service:**
   ```bash
   docker compose up -d
   ```

4. **Open the dashboard:**
   Navigate to `http://localhost:3001` (or your configured port).

5. **Create your admin account** on first visit — Uptime Kuma will prompt you to set up a username and password.

---

## Configuration Reference

| Variable | Default | Description |
|---|---|---|
| `UPTIME_KUMA_PORT` | `3001` | Host port for the Uptime Kuma web interface. Change this if port 3001 is already in use. |

All other configuration (monitors, notifications, status pages) is managed through the web UI after first launch. Uptime Kuma stores its settings in the SQLite database on the `/data` volume.

---

## Troubleshooting

**Container won't start or exits immediately**
Check logs with `docker compose logs uptime-kuma`. Common causes: port conflict on 3001, or the volume permissions are wrong. Ensure no other service is using the configured port.

**Health check shows unhealthy**
Uptime Kuma takes 20–40 seconds to initialize on first run. If it stays unhealthy, check that the container has enough memory (256MB minimum recommended) and that port 3001 is reachable inside the container.

**Can't access the web UI from another machine**
Verify the port mapping in `docker compose ps`. If using a firewall, ensure the configured `UPTIME_KUMA_PORT` is open. The default bind is `0.0.0.0`, so it should be accessible from any network interface.

**Notifications not sending**
Uptime Kuma's notification system is configured entirely through the web UI (Settings → Notifications). Test your notification setup using the "Test" button on the notification configuration page. Ensure the container has outbound network access to your notification provider.

**Upgrading Uptime Kuma**
Pull the latest image and recreate the container:
```bash
docker compose pull
docker compose up -d
```
Your data is stored on the volume and survives upgrades automatically.

---

## Backup & Recovery

Uptime Kuma stores all data (monitors, settings, notification configs, incident history) in an SQLite database inside the `/data` volume.

**Manual backup:**
```bash
docker exec uptime-kuma /bin/sh -c "sqlite3 /data/kuma.db '.backup /data/kuma-backup.db'"
docker cp uptime-kuma:/data/kuma-backup.db ./kuma-backup.db
```

**Full volume backup:**
```bash
docker run --rm -v uptime-kuma_data:/data -v $(pwd):/backup alpine tar czf /backup/uptime-kuma-backup.tar.gz -C /data .
```

**Restore:**
```bash
docker compose down
docker run --rm -v uptime-kuma_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/uptime-kuma-backup.tar.gz -C /data"
docker compose up -d
```

**Built-in backup:** Uptime Kuma also supports backup export/import from the web UI under Settings → Backup. Use this for migrating between instances or creating periodic exports.

---

## Links

- **Source code:** https://github.com/louislam/uptime-kuma
- **Documentation:** https://github.com/louislam/uptime-kuma/wiki
- **Docker image:** https://github.com/louislam/uptime-kuma/pkgs/container/uptime-kuma
- **Issues & feature requests:** https://github.com/louislam/uptime-kuma/issues
- **Community:** https://discord.gg/uptime-kuma
