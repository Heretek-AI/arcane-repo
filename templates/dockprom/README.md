# dockprom — Prometheus + Grafana Monitoring Stack

[dockprom](https://github.com/stefanprodan/dockprom) brings Prometheus metrics collection, Grafana dashboards, AlertManager notifications, cAdvisor container monitoring, and Node Exporter host metrics into a single `docker compose up`. Caddy reverse-proxies all web UIs behind a single port.

## Quick Start

1. **Start the stack:**

   ```bash
   docker compose up -d
   ```

2. **Access services** directly or through Caddy on port 80:

   | Service       | Direct URL                       | Via Caddy            |
   |---------------|----------------------------------|----------------------|
   | Grafana       | http://localhost:3000            | http://localhost:3000 |
   | Prometheus    | http://localhost:9090            | http://localhost:9090 |
   | AlertManager  | http://localhost:9093            | http://localhost:9093 |

3. **Log into Grafana** with the credentials from your `.env` (default: `admin` / `changeme`).

4. **Explore pre-configured targets** — Prometheus auto-discovers all services. Grafana is pre-wired with a Prometheus datasource.

## Architecture

```
                    ┌─────────────────────────────────┐
                    │           Caddy :80             │
                    │    (reverse proxy for all UIs)   │
                    └──────┬──────┬──────┬────────────┘
                           │      │      │
              ┌────────────┘      │      └────────────┐
              ▼                   ▼                   ▼
    ┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐
    │  Grafana :3000   │  │Prometheus:9090│  │AlertManager:9093 │
    │  (dashboards)    │  │  (metrics)    │  │  (notifications) │
    └────────┬─────────┘  └──────┬────────┘  └──────────────────┘
             │                   │
             │    ┌──────────────┼──────────────┐
             │    │              │              │
             │    ▼              ▼              ▼
             │  ┌──────────┐ ┌──────────┐ ┌──────────────┐
             │  │cAdvisor  │ │  Node    │ │ Pushgateway  │
             │  │ :8080    │ │ Exporter │ │   :9091      │
             │  │(container│ │ :9100    │ │ (batch jobs) │
             │  │ metrics) │ │(host OS) │ │              │
             │  └──────────┘ └──────────┘ └──────────────┘
             │
             └── (uses Prometheus datasource)
```

All 7 services share the `dockprom-net` bridge network. Config files are read-only bind mounts from `scripts/dockerfiles/dockprom/configs/` — no need to clone the upstream repo.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable               | Default    | Description                                    |
|------------------------|------------|------------------------------------------------|
| `GRAFANA_PORT`         | `3000`     | Host port for Grafana web UI                   |
| `GRAFANA_ADMIN_USER`   | `admin`    | Grafana admin username                         |
| `GRAFANA_ADMIN_PASSWORD`| `changeme`| Grafana admin password — **change for production**|
| `PROMETHEUS_PORT`      | `9090`     | Host port for Prometheus web UI and API        |
| `ALERTMANAGER_PORT`    | `9093`     | Host port for AlertManager web UI              |
| `PUSHGATEWAY_PORT`     | `9091`     | Host port for Pushgateway API                  |
| `CADVISOR_PORT`        | `8080`     | Host port for cAdvisor container metrics       |
| `CADDY_HTTP_PORT`      | `80`       | HTTP port for the Caddy reverse proxy          |

## Features

- **Prometheus**: Metrics collection and long-term storage with 15-day retention (configurable via `PROMETHEUS_RETENTION`)
- **Grafana**: Rich dashboards pre-wired to Prometheus — add community dashboards or build your own
- **AlertManager**: Alert routing with deduplication and grouping — configure Slack, email, PagerDuty in config
- **cAdvisor**: Per-container CPU, memory, disk, and network metrics from the Docker daemon
- **Node Exporter**: Host-level metrics (CPU, memory, disk, network, filesystem)
- **Pushgateway**: Accept metrics from ephemeral jobs, batch processes, and cron tasks
- **Caddy**: Automatic HTTPS-ready reverse proxy — serves all UIs through a single entry point

## cAdvisor Privileged Mode

cAdvisor requires `privileged: true` and `/dev/kmsg` device access to collect accurate container resource metrics. This is the standard upstream configuration — cAdvisor reads container cgroups and kernel metrics, not modifies them. If you do not need container-level metrics, you can comment out the cadvisor service in `docker-compose.yml`.

## Health Checks

All 7 services include Docker health checks:

```bash
# Check service health
docker compose ps

# Prometheus liveness
curl http://localhost:9090/-/healthy

# Grafana health
curl http://localhost:3000/api/health

# AlertManager health
curl http://localhost:9093/-/healthy

# cAdvisor health
curl http://localhost:8080/healthz

# Pushgateway health
curl http://localhost:9091/-/healthy
```

## Volume Management

- **prometheus_data**: Time-series metrics database
- **grafana_data**: Dashboards, user preferences, plugin data
- **caddy_data**: SSL certificates and Caddy state

Destroy all data: `docker compose down -v`

## Dependencies

| Service       | Depends On                                            |
|---------------|-------------------------------------------------------|
| prometheus    | (none — starts independently)                         |
| alertmanager  | (none — starts independently)                         |
| nodeexporter  | (none — starts independently)                         |
| cadvisor      | (none — starts independently)                         |
| grafana       | prometheus (healthy)                                  |
| pushgateway   | (none — starts independently)                         |
| caddy         | prometheus (healthy), grafana (healthy), alertmanager (healthy)|

## Upstream References

- [stefanprodan/dockprom](https://github.com/stefanprodan/dockprom) — Full upstream repository
- [Prometheus Docs](https://prometheus.io/docs/introduction/overview/)
- [Grafana Docs](https://grafana.com/docs/grafana/latest/)
- [cAdvisor Docs](https://github.com/google/cadvisor)
