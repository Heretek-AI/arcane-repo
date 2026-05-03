---
title: "PentaGI"
description: "AI penetration testing with autonomous security assessment"
---

# PentaGI

AI penetration testing with autonomous security assessment

## Tags

<a href="/categories/security" class="tag-badge">security</a> <a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/automation" class="tag-badge">automation</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pentagi/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pentagi/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/pentagi/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `pentagi` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `76d55b5a7474702aa1447b35bba0a3e99e7f3fd418b22c979bf837b05352bc70` |

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

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`. The container includes a healthcheck on port 8080 with a 60s start period.

