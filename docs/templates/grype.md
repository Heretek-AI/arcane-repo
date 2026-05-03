---
title: "Grype"
description: "Fast vulnerability scanner for container images and filesystems — produced by Anchore, matches CVEs against multiple databases including NVD, GitHub Advisory, and distro-specific feeds"
---

# Grype

Fast vulnerability scanner for container images and filesystems — produced by Anchore, matches CVEs against multiple databases including NVD, GitHub Advisory, and distro-specific feeds

## Tags

<a href="/categories/security" class="tag-badge">security</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grype/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grype/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/grype/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `grype` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `4e07b09a8221ee6fd073cf19d8326dde2c88658436b25b5fb0e4fc52dd94d03a` |

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

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `GRYPE_DB_CACHE_DIR` | `/root/.cache/grype/db` | Cache location for vulnerability database |
| `GRYPE_DB_AUTO_UPDATE` | `true` | Auto-update DB before each scan |
| `GRYPE_CHECK_FOR_APP_UPDATE` | `false` | Check for newer Grype version |
| `GRYPE_OUTPUT` | `table` | Output format: `table`, `json`, `cyclonedx` |
| `GRYPE_FAIL_ON_SEVERITY` | `critical` | Exit code 1 if vulns at or above this are found |

