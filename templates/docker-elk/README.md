# Docker ELK Stack — Elasticsearch + Logstash + Kibana

[The Docker ELK Stack](https://github.com/deviantony/docker-elk) brings the Elastic Stack to Docker Compose — centralized log aggregation with Elasticsearch, log processing pipelines with Logstash, and rich visualizations with Kibana. All three core services boot from official Elastic Docker images with a single `docker compose up`.

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

## Architecture (Simplified 4-Service Core)

| Service         | Role                                                                   | Port   |
|-----------------|------------------------------------------------------------------------|--------|
| **elasticsearch** | Document store and search engine — single-node cluster                 | 9200   |
| **logstash**    | Log processing pipeline — receives beats, parses, and indexes to ES    | 5044   |
| **kibana**      | Visualization and search UI — dashboards, discover, dev tools          | 5601   |
| **setup**       | One-time initialization container (profile: `setup`) — exits after completion | —      |

All services use official `docker.elastic.co` images pinned to `${ELK_VERSION}` (default: 8.17.0). Volume mounts reference bundled config files in `scripts/dockerfiles/docker-elk/configs/` — no need to clone the upstream repository.

## Optional Services (Upstream Profiles)

The [upstream docker-elk repository](https://github.com/deviantony/docker-elk) provides additional profiles for production deployments. These are **not included** in our simplified core but are documented here so you can extend your stack:

| Profile              | Services                                                  | Purpose                                     |
|----------------------|-----------------------------------------------------------|---------------------------------------------|
| `elk-monitoring`     | Metricbeat                                                 | Server-level metrics → Elasticsearch        |
| `elk-filebeat`       | Filebeat                                                   | Log shipper for container/host logs         |
| `elk-auditbeat`      | Auditbeat                                                  | System audit data collection                |
| `elk-heartbeat`      | Heartbeat                                                  | Uptime monitoring for services              |
| `elk-packetbeat`     | Packetbeat                                                 | Network packet analysis                     |
| `elk-apm-server`     | APM Server                                                 | Application performance monitoring          |
| `elk-enterprise-search` | Enterprise Search                                      | Full-text search experience (App Search, Workplace Search) |
| `elk-connectors`     | Connectors                                                 | Data sync connectors for third-party sources|
| `elk-elastic-agent`  | Elastic Agent, Fleet Server                                 | Centralized agent management                |
| `elk-fleet-proxy`    | Fleet Proxy                                                | Proxy for Fleet-managed agents              |

To add an optional service, copy its configuration from the [upstream repo](https://github.com/deviantony/docker-elk/tree/main/extensions) into your `scripts/dockerfiles/docker-elk/configs/` directory and merge the relevant service definitions into your compose file. Upstream profiles reference their config through the `extensions/` directory.

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

## Volume Management

- **elasticsearch_data**: Named Docker volume for persistent ES data.  
  Inspect: `docker volume inspect elasticsearch_data`  
  Remove (destroys all data): `docker compose down -v`

- **Config files**: Read-only bind mounts from `scripts/dockerfiles/docker-elk/configs/`. Edit these files on the host and restart services for changes to take effect.

## Health Checks

All three core services have Docker health checks:

```bash
# Elasticsearch cluster health
curl -s -u elastic:${ELASTIC_PASSWORD} http://localhost:9200/_cluster/health

# Logstash node stats
curl -s http://localhost:9600/_node/stats

# Kibana status
curl -s http://localhost:5601/api/status
```

For monitoring health in real time:

```bash
docker compose ps
```

## Resource Notes

- Elasticsearch requires sufficient memory: `ES_HEAP_SIZE` must be ≤ 50% of available RAM. The default `1g` heap needs at least 2 GB free RAM.
- Logstash pipelines that use persistent queues (`queue.type: persisted`) require additional disk space.
- The setup container runs once and exits. Set `RUN_SETUP=true` in `.env` and `docker compose --profile setup up setup` to re-run it.

## Upstream References

- [deviantony/docker-elk](https://github.com/deviantony/docker-elk) — Full upstream repository
- [Elastic Docs: Install with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)
- [Logstash Pipeline Reference](https://www.elastic.co/guide/en/logstash/current/pipeline.html)
