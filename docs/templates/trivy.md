---
title: "Trivy"
description: "Comprehensive vulnerability, misconfiguration, and secrets scanner for containers, filesystems, and Git repositories — scan images, IaC, and Kubernetes manifests"
---

# Trivy

Comprehensive vulnerability, misconfiguration, and secrets scanner for containers, filesystems, and Git repositories — scan images, IaC, and Kubernetes manifests

## Tags

<a href="/categories/security" class="tag-badge">security</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trivy/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trivy/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/trivy/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `trivy` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `42887747c15bbe94579d3b9ba7efa65edb23f0a05a049527632d68341e613e2a` |

## Quick Start

1. **Start the container:**

   ```bash
   docker compose up -d
   ```

2. **Scan a container image:**

   ```bash
   docker compose exec trivy trivy image nginx:latest
   ```

3. **Scan a filesystem:**

   ```bash
   docker compose exec trivy trivy fs /
   ```

4. **Scan a Git repository:**

   ```bash
   docker compose exec trivy trivy repo https://github.com/user/repo
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `TRIVY_CACHE_DIR` | `/root/.cache/trivy` | Cache location for vulnerability database |
| `TRIVY_QUIET` | `false` | Suppress progress output |
| `TRIVY_DEBUG` | `false` | Enable debug logging |
| `TRIVY_SEVERITY` | `CRITICAL,HIGH,MEDIUM` | Minimum severity to report |
| `TRIVY_TIMEOUT` | `5m0s` | Maximum scan duration |

