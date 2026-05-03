---
title: "dockprom"
description: "Complete monitoring stack — Prometheus metrics, Grafana dashboards, AlertManager notifications, cAdvisor container metrics, and Node Exporter host metrics, all reverse-proxied through Caddy"
---

# dockprom

Complete monitoring stack — Prometheus metrics, Grafana dashboards, AlertManager notifications, cAdvisor container metrics, and Node Exporter host metrics, all reverse-proxied through Caddy

## Tags

<a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/observability" class="tag-badge">observability</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dockprom/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dockprom/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dockprom/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dockprom` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `c80100380627097ef7a8113f95bb02346c25e2816ffa524dd9f853f91dc907b0` |

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

## Upstream

- [stefanprodan/dockprom](https://github.com/stefanprodan/dockprom) — Full upstream repository
- [Prometheus Docs](https://prometheus.io/docs/introduction/overview/)
- [Grafana Docs](https://grafana.com/docs/grafana/latest/)
- [cAdvisor Docs](https://github.com/google/cadvisor)

