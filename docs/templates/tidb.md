---
title: "TiDB"
description: "Distributed SQL database with MySQL compatibility and HTAP capabilities"
---

# TiDB

Distributed SQL database with MySQL compatibility and HTAP capabilities

## Tags

<a href="/categories/database" class="tag-badge">database</a> <a href="/categories/sql" class="tag-badge">sql</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tidb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tidb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tidb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tidb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `bec1126810ee5d36aab0e1f278b00250b11cc94248724824d8300408894e361c` |

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

   Open [http://localhost:4000](http://localhost:4000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

