# Firecrawl

Self-hosted [Firecrawl](https://github.com/firecrawl/firecrawl) web scraping API:
scrape pages, crawl sites, map URLs, and run AI-powered extraction for your agents.

## Deployment

1. Deploy this template from your Arcane registry.
2. Set `POSTGRES_PASSWORD` to a strong unique value before the first start.
3. Open the API at `http://<host>:3002` (or your configured `PORT`).
4. Run your first scrape:
   ```bash
   curl -X POST http://<host>:3002/v2/scrape \
     -H 'Content-Type: application/json' \
     -d '{"url": "https://example.com", "formats": ["markdown"]}'
   ```

Keep the first run on the baseline: `USE_DB_AUTHENTICATION=false`, the bundled
NuQ PostgreSQL queue, bundled Playwright, and no model provider. AI-backed
features (extract, summarize) need `OPENAI_API_KEY` (or an OpenAI-compatible
endpoint / Ollama) configured afterwards.

## Production notes

- The default API is **unauthenticated**. Add authentication, TLS termination,
  and network policy before exposing it outside a trusted network.
- Queue data persists in named volumes (`redis-data`, `rabbitmq-data`,
  `nuq-postgres-data`). Plan backups and upgrades for them.
- Keep PostgreSQL on its defaults unless you change the API and database values
  together; the bundled `pg_cron` setup targets the default `postgres` database.
- Enable the Bull queue UI only with a strong `BULL_AUTH_KEY` and restricted
  network access.
- Resource defaults (`playwright-service` 2 CPU / 4 GB) reflect real scraping
  load; raise them if you increase `CRAWL_CONCURRENT_REQUESTS`.

## Deviations from upstream

- Upstream `docker-compose.yaml` uses local `build:` contexts; this template
  uses the prebuilt images (`ghcr.io/firecrawl/firecrawl`,
  `ghcr.io/firecrawl/playwright-service`, `ghcr.io/firecrawl/nuq-postgres`)
  so Arcane can deploy without the Firecrawl source tree.
- The experimental FoundationDB queue backend is omitted; NuQ PostgreSQL is the
  supported queue.
- Redis runs with `--appendonly yes` and all stateful services use named
  volumes; upstream defines no persistent volumes for them.
- Stateful images keep major-version pins (`redis:7-alpine`,
  `rabbitmq:3-management`); Firecrawl images track `:latest`.
