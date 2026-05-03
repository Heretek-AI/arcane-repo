---
title: "WorldMonitor"
description: "Real-time global monitoring and alerting system"
---

# WorldMonitor

Real-time global monitoring and alerting system

## Tags

<a href="/categories/monitoring" class="tag-badge">monitoring</a> <a href="/categories/analytics" class="tag-badge">analytics</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/worldmonitor/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/worldmonitor/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/worldmonitor/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `worldmonitor` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `6eef0c49f740662718a1e915ccbcca41e2ba68d262903071fee1f18cf184f727` |

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

The docker-compose.yml exposes environment variables documented in `.env.example`.

> **Status: 🏗️ CI Build Pending**
> The upstream project includes a Dockerfile, but no pre-built image is published. The template currently
> references a non-existent image. A CI pipeline will build and publish to GHCR (planned for future update).

