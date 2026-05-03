---
title: "OpenBB"
description: "Open-source investment research platform with AI-powered trading strategies"
---

# OpenBB

Open-source investment research platform with AI-powered trading strategies

## Tags

<a href="/categories/analytics" class="tag-badge">analytics</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openbb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openbb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/openbb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `openbb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `10a40409bdbc70b337959d7a2184c5b03f0f295a764046798719c26b01198cf5` |

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

