---
title: "Netdata"
description: "Real-time monitoring with metrics, dashboards, and alerts"
---

# Netdata

Real-time monitoring with metrics, dashboards, and alerts

## Tags

<a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/observability" class="tag-badge">observability</a> <a href="/categories/devops" class="tag-badge">devops</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netdata/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netdata/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/netdata/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `netdata` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `81cbec300d30bca41574c047318607aafb11003209f3d23873de1edd72157125` |

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the service:**

   Open [http://localhost:19999](http://localhost:19999) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

