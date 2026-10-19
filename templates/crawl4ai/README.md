# Crawl4AI

Self-hosted [Crawl4AI](https://github.com/unclecode/crawl4AI) web crawler for
LLMs and AI agents: scrape pages to clean markdown, capture screenshots and
PDFs, run LLM-powered extraction, and call it all from REST or
[Model Context Protocol](https://docs.crawl4ai.com) clients.

## Deployment

1. Deploy this template from your Arcane registry.
2. Set `CRAWL4AI_API_TOKEN` to a strong unique value before the first start.
   The server refuses a non-loopback bind without a credential, so the API is
   unreachable until the token is set. Send it as `Authorization: Bearer <token>`
   on every request except `/health`.
3. Open the API at `http://<host>:11235` (or your configured `PORT`) and try:
   ```bash
   curl -X POST http://<host>:11235/crawl \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <token>" \
     -d '{"urls": ["https://example.com"]}'
   ```
4. The interactive playground lives at `http://<host>:11235/playground` and the
   MCP endpoints at `/mcp/sse` and `/mcp/ws`.

Keep the first run on the baseline: deep crawling off, `/execute_js` and hooks
off, and no model provider. LLM-backed extraction needs a provider key
(`OPENAI_API_KEY` or equivalent, plus optional `LLM_PROVIDER`) configured
afterwards.

## Production notes

- The API is **unauthenticated until you set `CRAWL4AI_API_TOKEN`**. Add TLS
  termination and network policy before exposing it outside a trusted network.
- Deep crawling is off by default (`CRAWL4AI_ALLOW_DEEP_CRAWL=false`). Turn it
  on only when you accept that one request can fetch many pages; page and depth
  budgets are clamped server-side.
- `/execute_js` and declarative hooks stay disabled. They run caller-supplied
  code and are an RCE risk on a shared server.
- Browser state, queue data, and screenshots live on ephemeral container
  storage (read-only root with tmpfs); plan for them being wiped on
  redeploy, and keep crawl artifacts client-side if you need them.
- Resource defaults (1 GB shm, 4 GB memory limit) reflect real Chromium load;
  give the host at least 4 GB of RAM and raise limits for heavy concurrent use.

## Deviations from upstream

- Upstream `docker-compose.yml` supports local `build:` contexts and
  `IMAGE`/`TAG` overrides; this template uses the prebuilt image
  (`unclecode/crawl4ai:latest`) so Arcane can deploy without the Crawl4AI
  source tree.
- Upstream reads LLM keys from an optional `.llm.env` file; this template
  passes the same variables through `environment:` so they are set in the
  Arcane project environment instead.
- The TLS-weakening (`CRAWL4AI_ALLOW_INSECURE_TLS`) and internal-URL
  (`CRAWL4AI_ALLOW_INTERNAL_URLS`) flags are intentionally omitted; the
  template keeps the upstream SSRF/TLS protections on.
