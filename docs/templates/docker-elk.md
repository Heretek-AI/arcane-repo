---
title: "Docker ELK Stack"
description: "Elasticsearch, Logstash, and Kibana stack for centralized log aggregation, search, and visualization — production-ready with health checks on all core services"
---

# Docker ELK Stack

Elasticsearch, Logstash, and Kibana stack for centralized log aggregation, search, and visualization — production-ready with health checks on all core services

## Tags

<a href="/categories/observability" class="tag-badge">observability</a> <a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/analytics" class="tag-badge">analytics</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-elk/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-elk/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/docker-elk/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `docker-elk` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dd581a29fd5ff41271b115c70fa0c5848fe73fec89fa4c48719c239ae04becf8` |

## Architecture

| Service         | Role                                                                   | Port   |
|-----------------|------------------------------------------------------------------------|--------|
| **elasticsearch** | Document store and search engine — single-node cluster                 | 9200   |
| **logstash**    | Log processing pipeline — receives beats, parses, and indexes to ES    | 5044   |
| **kibana**      | Visualization and search UI — dashboards, discover, dev tools          | 5601   |
| **setup**       | One-time initialization container (profile: `setup`) — exits after completion | —      |

All services use official `docker.elastic.co` images pinned to `${ELK_VERSION}` (default: 8.17.0). Volume mounts reference bundled config files in `scripts/dockerfiles/docker-elk/configs/` — no need to clone the upstream repository.

## Quick Start

1. **Prepare your configuration:**

   ```bash
   cp .env.example .env
   # Set ELASTIC_PASSWORD to a strong password
   # Set KIBANA_ENCRYPTION_KEY via: openssl rand -hex 32
   ```

2. **Start the core stack:**

   ```bash
   docker compose up -d
   ```

3. **Run one-time setup** (creates the kibana_system user, ILM policies, and index templates):

   ```bash
   docker compose --profile setup up setup
   ```

4. **Access Kibana** at [http://localhost:5601](http://localhost:5601).  
   Username: `elastic` — Password: the value of `ELASTIC_PASSWORD` from your `.env`.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                | Default    | Description                                          |
|-------------------------|------------|------------------------------------------------------|
| `ELK_VERSION`           | `8.17.0`   | Elastic Stack version for all three services          |
| `ES_HEAP_SIZE`          | `1g`       | Elasticsearch JVM heap (-Xms and -Xmx)               |
| `ELASTIC_PASSWORD`      | `changeme` | Elastic superuser password — **change for production**|
| `ES_PORT`               | `9200`     | Host port for Elasticsearch HTTP API                 |
| `LOGSTASH_BEATS_PORT`   | `5044`     | Host port for Logstash Beats input                   |
| `KIBANA_PORT`           | `5601`     | Host port for Kibana web interface                   |
| `KIBANA_ENCRYPTION_KEY` | (empty)    | 256-bit encryption key for Kibana saved objects      |
| `RUN_SETUP`             | `true`     | Controls whether the setup container runs             |

### Generating a Kibana Encryption Key

```bash
openssl rand -hex 32
```

### Sending Logs

Point Filebeat, Winlogbeat, or any Beats shipper at `localhost:5044` (the Logstash Beats input port). The default pipeline indexes into Elasticsearch under the `logs-YYYY.MM.dd` index pattern. Customize `scripts/dockerfiles/docker-elk/configs/logstash/pipeline/logstash.conf` for your log formats.

## Upstream

- [deviantony/docker-elk](https://github.com/deviantony/docker-elk) — Full upstream repository
- [Elastic Docs: Install with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
- [Logstash Pipeline Reference](https://www.elastic.co/guide/en/logstash/current/pipeline.html)

