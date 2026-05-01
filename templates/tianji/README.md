# Tianji — All-in-One Website Analytics & Monitoring

[Tianji](https://github.com/msgbyte/tianji) combines website analytics, uptime monitoring, and server status reporting into a single self-hosted dashboard. Privacy-first — all data stays on your infrastructure.

## Quick Start

1. **Start the services:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:12345](http://localhost:12345)

3. **Create your admin account** on first launch, then set `TIANJI_ALLOW_REGISTER=false` in `.env` to lock it down.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                | Default    | Description                                   |
|-------------------------|------------|-----------------------------------------------|
| `TIANJI_PORT`           | `12345`    | Host port for the web dashboard               |
| `TIANJI_DB_NAME`        | `tianji`   | PostgreSQL database name                      |
| `TIANJI_DB_USER`        | `tianji`   | PostgreSQL user                               |
| `TIANJI_DB_PASSWORD`    | `changeme` | PostgreSQL password — **change for production**|
| `TIANJI_JWT_SECRET`     | (empty)    | JWT signing secret — **required**             |
| `TIANJI_ALLOW_REGISTER` | `true`     | Allow new user registration (disable after setup)|

## Architecture

- **tianji-app**: Node.js application — serves the web dashboard, API, background workers for uptime checks and telemetry processing
- **tianji-db**: PostgreSQL 15.4 — stores analytics events, uptime results, user accounts, and configuration

## Features

- **Website analytics**: Track page views, sessions, events, and user journeys
- **Uptime monitoring**: HTTP, TCP, and DNS checks with customizable intervals and alert thresholds
- **Server status**: CPU, memory, disk, and network monitoring with historical charts
- **Telemetry SDK**: Lightweight client for custom telemetry from your own services
- **Notification channels**: Email, webhook, and Telegram alerts for status changes

## Health Check

```bash
curl -s http://localhost:12345/api/health
```

Full documentation: [github.com/msgbyte/tianji](https://github.com/msgbyte/tianji)
