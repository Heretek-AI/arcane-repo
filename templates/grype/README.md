# Grype — Vulnerability Scanner for Containers and Filesystems

[Grype](https://github.com/anchore/grype) (12,112 ★) by Anchore is a fast, easy-to-use vulnerability scanner for container images and filesystems. It cross-references packages against multiple vulnerability databases including NVD, GitHub Advisory, and distro-specific feeds.

Grype is a CLI-only tool — this template runs it as a `sleep infinity` container. All interaction is via `docker compose exec`.

## Quick Start

1. **Start the container:**

   ```bash
   docker compose up -d
   ```

2. **Scan a container image:**

   ```bash
   docker compose exec grype grype nginx:latest
   ```

3. **Scan a directory:**

   ```bash
   docker compose exec grype grype dir:/
   ```

4. **Scan with JSON output:**

   ```bash
   docker compose exec grype grype python:3.12-slim -o json
   ```

## Common Commands

| Command | Description |
|---------|-------------|
| `grype <image>` | Scan a container image for vulnerabilities |
| `grype dir:<path>` | Scan a directory or filesystem |
| `grype sbom:<file>` | Scan an SBOM file (CycloneDX, SPDX) |
| `grype <image> -o json` | Output results as JSON |
| `grype <image> -o cyclonedx` | Output results as CycloneDX SBOM |
| `grype --help` | Show all commands and flags |

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `GRYPE_DB_CACHE_DIR` | `/root/.cache/grype/db` | Cache location for vulnerability database |
| `GRYPE_DB_AUTO_UPDATE` | `true` | Auto-update DB before each scan |
| `GRYPE_CHECK_FOR_APP_UPDATE` | `false` | Check for newer Grype version |
| `GRYPE_OUTPUT` | `table` | Output format: `table`, `json`, `cyclonedx` |
| `GRYPE_FAIL_ON_SEVERITY` | `critical` | Exit code 1 if vulns at or above this are found |

## Scanning Local Images

The Docker socket is mounted so Grype can scan images in the host Docker daemon:

```bash
docker pull node:22-alpine
docker compose exec grype grype node:22-alpine
```

## Scanning the Current Directory

The current directory is mounted at `/scan-target` as read-only:

```bash
docker compose exec grype grype dir:/scan-target
```

## Comparison with Trivy

Grype focuses specifically on vulnerability detection with multiple database sources. Trivy additionally covers misconfigurations and secrets. Use both for defense-in-depth.

Official docs: [github.com/anchore/grype#readme](https://github.com/anchore/grype#readme)
