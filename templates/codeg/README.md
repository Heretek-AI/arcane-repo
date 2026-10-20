# Codeg

Self-hosted [Codeg](https://github.com/spacering-net/codeg) multi-agent coding
workspace: run Claude Code, Codex, Gemini CLI, OpenCode and more from one web
UI, with session search, multi-agent delegation, and desktop/mobile clients.

## Deployment

1. Deploy this template from your Arcane registry.
2. Set `CODEG_TOKEN` to a strong unique value before the first start. (If left
   empty the server generates and persists one; `docker logs` shows it.)
3. Open the workbench at `http://<host>:3080` (or your configured `PORT`) and
   enter the token.
4. Mount your code so agents have something to work on: add a bind mount such
   as `- /path/to/projects:/projects` to the `codeg` service volumes, then
   open `/projects/<app>` as a workspace. Without it agents only see the
   container's empty filesystem.
5. Agent CLIs are downloaded into the data volume on first use; model API keys
   are configured in-app per agent, not via environment variables.

Keep the first run on the baseline: port bridge `3081-3090` published, no
hostname pattern, default filesystem policy, and no extra mounts beyond
`/projects`.

## Production notes

- The web UI and API share one bearer token (`CODEG_TOKEN`). Add TLS
  termination and network policy before exposing the port outside a trusted
  network; the dev-server bridge ports (`3081-3090`) too.
- All state (SQLite `codeg.db`, auth tokens, logs, uploads, downloaded agent
  binaries) lives in the `codeg-data` volume. Back it up; a single volume
  covers everything. Do not set `CODEG_HOME` to a different root — the server
  warns and state silently splits across two filesystems.
- In-place upgrades (Settings → Software Update) rewrite the binaries inside
  the running container only; recreating the container drops the upgrade.
  Pull a new image and recreate to make an upgrade permanent.
- Behind a reverse proxy, prefer `CODEG_BRIDGE_HOST_PATTERN=auto` (needs a
  wildcard DNS record and vhost pointing at `:3080`) over publishing the port
  range; the range publish in `compose.yaml` is then unused and can be dropped.
- `CODEG_COMPUTER_USE` is intentionally unwired: it shares the server's own
  screen with agents, which is meaningless on a headless host. Leave it off in
  Docker.
- There is no anonymous health endpoint (`/health` requires the token), so the
  template ships no healthcheck, matching upstream.

## Advanced knobs (unwired, add to `environment:` if needed)

- `CODEG_ACP_IDLE_TIMEOUT_SECS` — agent idle-disconnect timeout (default 60s,
  `0` disables idle disconnects but not disk reclamation).
- `CODEG_UPLOAD_MAX_TOTAL_BYTES` / `CODEG_UPLOAD_QUOTA_STRICT` — cap total
  upload bytes on shared deployments; strict aborts startup on a typo.
- `CODEG_BACKUP_UPLOAD_MAX_BYTES` — cap restore-upload size.
- `CODEG_LOG` / `CODEG_LOG_MAX_FILES` — log level override and retention.
- `CODEG_ACP_TMP_ROOT` / `CODEG_ACP_TMP_ISOLATION=0` — relocate agent scratch
  dirs or share the ambient temp directory.
- `CODEG_WORKSPACE_*_CONCURRENCY` — transfer parallelism tuning.

## Deviations from upstream

- Upstream `docker-compose.yml` uses a local `build:` context; this template
  uses the prebuilt image (`ghcr.io/spacering-net/codeg:latest`) so Arcane can
  deploy without the Codeg source tree.
- `CODEG_PORT`, `CODEG_HOST`, `CODEG_DATA_DIR`, `CODEG_STATIC_DIR`, and `SHELL`
  are pinned to the image's baked values instead of being user-configurable.
- The `/projects` bind mount stays commented: every host path differs, so the
  operator adds the line that matches their machine.
- Agent filesystem guardrails (`CODEG_ACP_FS_POLICY`, `CODEG_ACP_FS_EXTRA_ROOTS`)
  are wired with empty (default) values; the remaining tuning knobs above are
  documented here rather than wired, unlike upstream's fully-commented compose
  file.
- No healthcheck: upstream defines none, and `/health` requires authentication.
