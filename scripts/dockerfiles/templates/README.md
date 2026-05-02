# Dockerfile Templates

Parameterized Dockerfile templates using Python's `string.Template` for the
Arcane custom-build pipeline. Each template captures the core pattern for a
Dockerfile family; per-template variables produce concrete Dockerfiles.

## Template Files

| Template | Pattern | Dockerfiles |
|----------|---------|-------------|
| `uv-python.Dockerfile.template` | Python apps using uv (clone + pip) | 10 |
| `node-alpine.Dockerfile.template` | Node.js/Bun apps (multi-stage) | 5 |

## Patterns

### 1. uv-python Pattern

Single-stage build using `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.
Clones upstream repo, installs Python deps via `uv pip install`, exposes port.

**Variables (6):**

| Variable | Description | Example |
|----------|-------------|---------|
| `UPSTREAM_REPO` | Git clone URL | `https://github.com/onyx-dot-app/onyx.git` |
| `APP_SLUG` | Short name for temp dir | `onyx` |
| `EXTRA_PACKAGES` | Additional pip packages | `uvicorn fastapi` |
| `EXPOSE_PORT` | Container port | `8080` |
| `ENV_PREFIX` | Env var prefix for PORT | `ONYX` |
| `CMD_MODULE` | uvicorn module path | `onyx.main:app` |

**Dockerfiles using this pattern:**
astrbot, kag, memvid, mlflow, nanobot, onyx, rd-agent, streamer-sales, trendradar, yuxi

### 2. node-alpine Pattern

Multi-stage build: builder stage (clone + install + build) and runtime stage.
Supports both npm and bun as build tools via `$BUILD_TOOL`.

**Core variables (9):**

| Variable | Description | Example |
|----------|-------------|---------|
| `BUILDER_IMAGE` | Base image for builder | `node:20-slim` |
| `RUNTIME_IMAGE` | Base image for runtime | `node:lts-alpine` |
| `UPSTREAM_REPO` | Git clone URL | `https://github.com/SillyTavern/SillyTavern.git` |
| `APP_SLUG` | Short name for temp dir | `st` |
| `BUILD_TOOL` | npm or bun | `npm` |
| `BUILD_CMD` | Build command | `npm run build` |
| `EXPOSE_PORT` | Container port | `8000` |
| `ENTRYPOINT_CMD` | CMD argument(s) | `node server.js` |
| `EXTRA_DEPS` | System packages for builder | `libc6-compat` |

**Block variables (8, optional):**

| Variable | Description | Default |
|----------|-------------|---------|
| `SYSTEM_DEPS` | System package install for builder | apt-get with git + ca-certificates |
| `BUN_SETUP` | Bun installation command | (empty) |
| `INSTALL_CMD` | Dependency install command | `$BUILD_TOOL install` |
| `BUILD_CMD_BLOCK` | Build command block | `RUN $BUILD_CMD` |
| `RUNTIME_SYSTEM_DEPS` | System deps for runtime | apt-get with ca-certificates |
| `COPY_CMD` | COPY from builder | `COPY --from=builder /app /app` |
| `ENV_BLOCK` | ENV declarations | (empty) |
| `HEALTHCHECK_CMD` | HEALTHCHECK directive | (empty) |

**Dockerfiles using this pattern:**
aionui, cc-gateway, rowboat, sillytavern, vane

### 3. Custom Pattern

Nine Dockerfiles are too heterogeneous for code templating. Each has unique
build requirements (Rust compilation, Java/Maven, Go binaries, multi-service
architectures). Document patterns only; no template.

**Custom-build Dockerfiles:** cog, plexe, tradingagents, clawith, harbor-llm,
om1, openfang, sunshine, wgcloud

**Common traits:**
- Base images: `python:3.12-slim`, `rust:1-slim-bookworm`, `ubuntu:22.04`,
  `maven:3.9-eclipse-temurin-11`, `golang:1.26-alpine`
- Multi-stage builds with language-specific toolchains
- FastAPI wrapper server (`server.py`) for /health + /info endpoints
- COPY server.py from `scripts/dockerfiles/<id>/server.py`

### 4. Config-Bundle Pattern

Two templates have no Dockerfile — they are pure configuration bundles:

- **docker-elk**: Elasticsearch + Logstash + Kibana configs
- **dockprom**: Prometheus + Grafana + Alertmanager + Caddy configs

Validation for these is config-file presence, not Dockerfile syntax.

## Usage

### Generating a Dockerfile from a template

```python
from string import Template
from pathlib import Path

# Load template
tmpl = Template(Path("scripts/dockerfiles/templates/uv-python.Dockerfile.template").read_text())

# Define variables
variables = {
    "UPSTREAM_REPO": "https://github.com/example/app.git",
    "APP_SLUG": "myapp",
    "EXTRA_PACKAGES": "fastapi uvicorn",
    "EXPOSE_PORT": "8000",
    "ENV_PREFIX": "MYAPP",
    "CMD_MODULE": "myapp.server:app",
}

# Generate
dockerfile = tmpl.safe_substitute(variables)
print(dockerfile)
```

### Verifying templates

```bash
python scripts/verify-templates.py           # run all checks
python scripts/verify-templates.py --verbose  # show generated Dockerfiles
python scripts/verify-templates.py --strict   # fail on warnings too
```

The verification script:
1. Loads each template file
2. Applies variable definitions for 15 known Dockerfiles
3. Validates generated Dockerfile syntax (FROM, WORKDIR, EXPOSE, CMD)
4. Checks directive ordering
5. Verifies no unresolved template variables remain

## Checklist: Creating a New Custom-Build Template

1. **Identify the pattern.** Does the Dockerfile fit uv-python or node-alpine?
   If not, it's a custom build — document the pattern only.

2. **For uv-python/node-alpine patterns:**
   - [ ] Add variable definitions to `verify-templates.py`
   - [ ] Run `python scripts/verify-templates.py` — must pass
   - [ ] Add the Dockerfile to `scripts/dockerfiles/<id>/Dockerfile`
   - [ ] Create `server.py` with /health + /info endpoints
   - [ ] Create `docker-compose.yml` referencing `ghcr.io/heretek-ai/arcane-repo/<id>:latest`
   - [ ] Create CI workflow at `.github/workflows/build-<id>.yml`

3. **For custom builds:**
   - [ ] Document the build pattern in comments at top of Dockerfile
   - [ ] Ensure multi-stage build produces minimal runtime image
   - [ ] Include FastAPI wrapper server for /health + /info
   - [ ] Create CI workflow with GHCR push

4. **For config bundles:**
   - [ ] Place configs in `scripts/dockerfiles/<id>/configs/`
   - [ ] Create `docker-compose.yml` referencing public images
   - [ ] Validate config files exist (no Dockerfile needed)

## Template Design Principles

- **safe_substitute()** is used (not substitute()) — undefined variables become
  empty strings rather than raising errors
- **Block variables** use the `$VAR` form (not `${VAR}`) for consistency
- **Comments** in templates document variable purposes and are preserved in output
- **Defaults** are encoded in the variable definitions, not the template itself
- **Round-trip fidelity** is structural, not character-by-character — templates
  capture the core pattern; project-specific customizations are in the actual Dockerfile
