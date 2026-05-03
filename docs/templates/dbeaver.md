---
title: "DBeaver"
description: "Universal database tool for MySQL, PostgreSQL, SQLite, Oracle, SQL Server"
---

# DBeaver

Universal database tool for MySQL, PostgreSQL, SQLite, Oracle, SQL Server

## Tags

<a href="/categories/database" class="tag-badge">database</a> <a href="/categories/tools" class="tag-badge">tools</a> <a href="/categories/sql" class="tag-badge">sql</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dbeaver/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dbeaver/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/dbeaver/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `dbeaver` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `3e6f9a59720296afde7479bfc97cfa8efc3b124b2802d902767fe416d3fc63c3` |

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

