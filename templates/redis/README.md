# Redis

In-memory data store used as a database, cache, message broker, and streaming engine for high-performance applications.

## Project Overview

[Redis](https://redis.io/) is an open-source, in-memory data structure store that can be used as a database, cache, message broker, and streaming engine. It supports a wide range of data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes, and streams.

This template runs a standalone Redis instance with persistent storage and a built-in health check. It's suitable for:

- **Caching** — session stores, page caching, query result caching
- **Message brokering** — pub/sub patterns, task queues via lists
- **Real-time analytics** — counters, rate limiting, leaderboards
- **Session management** — user sessions, token storage
- **Streaming** — event logs, activity feeds via Redis Streams

For production deployments requiring high availability or clustering, see the [Redis Cluster documentation](https://redis.io/docs/operate/oss_and_stack/management/scaling/).

## Architecture

| Component | Details |
|-----------|---------|
| **Image** | `redislabs/redis:latest` |
| **Container** | `redis` |
| **Port** | `8080` (configurable via `REDIS_PORT`) |
| **Volume** | `redis_data` → `/data` (persistent storage) |
| **Health check** | `redis-cli ping` every 30s, 3 retries, 10s start period |
| **Restart policy** | `unless-stopped` |

### Data persistence

Redis writes an RDB snapshot to `/data` inside the container, backed by the `redis_data` named volume. This volume survives container restarts and removals. See [Backup & Recovery](#backup--recovery) for how to protect this data.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Verify it's running:**

   ```bash
   docker compose ps
   ```

   The health check should show `healthy` after ~10 seconds.

4. **Connect to Redis:**

   ```bash
   docker compose exec redis redis-cli
   ```

   Then try a basic command:

   ```
   127.0.0.1:6379> SET hello "world"
   OK
   127.0.0.1:6379> GET hello
   "world"
   ```

## Configuration Reference

All variables are set in your `.env` file.

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_PORT` | `8080` | Host port mapped to the Redis service. Change this if port 8080 is already in use. |

### Runtime configuration

To pass additional Redis configuration at startup, you can extend the `docker-compose.yml` command:

```yaml
services:
  redis:
    image: docker.io/redislabs/redis:latest
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
```

Common options:

| Option | Example | Description |
|--------|---------|-------------|
| `--appendonly yes` | Enables AOF persistence (survives more failure scenarios than RDB alone) |
| `--maxmemory 256mb` | Limits Redis memory usage |
| `--maxmemory-policy allkeys-lru` | Eviction policy when maxmemory is reached |
| `--requirepass <secret>` | Requires authentication for all connections |

### Adding authentication

To password-protect your Redis instance, add a `command` override and pass the password via environment variable:

```yaml
services:
  redis:
    command: redis-server --requirepass ${REDIS_PASSWORD}
    environment:
      - REDIS_PASSWORD=${REDIS_PASSWORD}
```

Then add to `.env`:

```
REDIS_PASSWORD=your-strong-password-here
```

## Troubleshooting

### Container won't start / exits immediately

Check logs:

```bash
docker compose logs redis
```

Common causes:
- **Port conflict** — another service is using the configured `REDIS_PORT`. Change it in `.env`.
- **Corrupted data** — if the RDB file is corrupted, Redis will refuse to start. See [Recovery from corrupted data](#recovery-from-corrupted-data).

### Health check shows unhealthy

The health check runs `redis-cli ping` and expects a `PONG` response. If it fails:

```bash
docker compose exec redis redis-cli ping
```

- If this returns `PONG`, the issue is likely timing — wait for the start period to pass.
- If it returns a connection error, Redis may be overloaded or misconfigured.

### Slow performance

- Check memory usage: `docker compose exec redis redis-cli info memory`
- Check connected clients: `docker compose exec redis redis-cli info clients`
- Ensure the host has enough RAM — Redis keeps all data in memory.

### Connection refused from other containers

Other containers on the same Docker network should connect via hostname `redis` on the internal port (6379), not the mapped host port. Example connection string:

```
redis://redis:6379
```

## Backup & Recovery

### Backup

Redis snapshots (RDB files) are stored in the `redis_data` volume at `/data`. To create a backup:

1. **Trigger a snapshot:**

   ```bash
   docker compose exec redis redis-cli BGSAVE
   ```

2. **Copy the dump file out of the container:**

   ```bash
   docker cp redis:/data/dump.rdb ./dump.rdb
   ```

3. **For AOF-enabled instances, also copy the AOF file:**

   ```bash
   docker cp redis:/data/appendonly.aof ./appendonly.aof
   ```

### Automated backups

Add a cron job on the host to periodically dump and archive:

```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker compose -f /path/to/docker-compose.yml exec -T redis redis-cli BGSAVE
sleep 5
docker cp redis:/data/dump.rdb /backups/redis/dump_${TIMESTAMP}.rdb
find /backups/redis -name "dump_*.rdb" -mtime +7 -delete
```

### Recovery

1. **Stop the container:**

   ```bash
   docker compose down
   ```

2. **Copy the backup into the volume:**

   ```bash
   docker run --rm -v redis_data:/data -v $(pwd):/backup alpine cp /backup/dump.rdb /data/dump.rdb
   ```

3. **Restart:**

   ```bash
   docker compose up -d
   ```

### Recovery from corrupted data

If Redis won't start due to a corrupted RDB or AOF file:

1. Stop the container: `docker compose down`
2. Remove the corrupted data:
   ```bash
   docker run --rm -v redis_data:/data alpine sh -c "rm -f /data/dump.rdb /data/appendonly.aof"
   ```
3. Restart: `docker compose up -d`

**Warning:** This deletes all data. Only do this if you have no usable backup.

## Links

- **Source code:** [https://github.com/redis/redis](https://github.com/redis/redis)
- **Documentation:** [https://redis.io/docs/](https://redis.io/docs/)
- **Commands reference:** [https://redis.io/docs/latest/commands/](https://redis.io/docs/latest/commands/)
- **Docker Hub:** [https://hub.docker.com/r/redislabs/redis](https://hub.docker.com/r/redislabs/redis)
- **Community:** [https://redis.io/community/](https://redis.io/community/)
