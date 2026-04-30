# Pulse — AI-Powered Infrastructure Monitoring

[Pulse](https://github.com/rcourtman/Pulse) provides real-time server monitoring with AI-powered insights. Track CPU, memory, disk, and network metrics, detect anomalies automatically, and receive intelligent alerts.

## Quick Start

1. **Start the services:**

   ```bash
   docker compose up -d
   ```

2. **Access the dashboard** at [http://localhost:8080](http://localhost:8080)

3. **Add your servers** from the dashboard to begin monitoring.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable              | Default    | Description                                   |
|-----------------------|------------|-----------------------------------------------|
| `PULSE_PORT`          | `8080`     | Host port for the web dashboard               |
| `PULSE_DB_NAME`       | `pulse`    | PostgreSQL database name                      |
| `PULSE_DB_USER`       | `pulse`    | PostgreSQL user                               |
| `PULSE_DB_PASSWORD`   | `changeme` | PostgreSQL password — **change for production**|
| `PULSE_SECRET_KEY`    | (empty)    | Session encryption secret — **required**      |
| `PULSE_LOG_LEVEL`     | `info`     | Log verbosity (debug, info, warn, error)      |

## Architecture

- **pulse-app**: The main application — web dashboard, API, metric processing, AI anomaly detection
- **pulse-db**: PostgreSQL database — stores metrics, configuration, and user data
- **pulse-redis**: Redis cache — handles real-time metric ingestion, job queues, and session caching

## Features

- **Real-time monitoring**: CPU, memory, disk I/O, network bandwidth
- **AI anomaly detection**: Automatically learn normal patterns and detect deviations
- **Intelligent alerting**: Reduce noise with smart alert grouping and escalation
- **Historical analysis**: Query and visualize historical metrics with trend detection

## Health Check

```bash
curl http://localhost:8080/api/health
```

Full documentation: [github.com/rcourtman/Pulse](https://github.com/rcourtman/Pulse)
