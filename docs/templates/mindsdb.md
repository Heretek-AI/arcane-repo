---
title: "MindsDB"
description: "AI database that enables you to build, train, and deploy ML models using SQL"
---

# MindsDB

AI database that enables you to build, train, and deploy ML models using SQL

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/database" class="tag-badge">database</a> <a href="/categories/sql" class="tag-badge">sql</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mindsdb/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mindsdb/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mindsdb/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mindsdb` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `ce6ba04ea29c3c459c3d68bcc6eee9bf8421c762c5b178c4f8867e57ac717333` |

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

   Open [http://localhost:47334](http://localhost:47334) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

