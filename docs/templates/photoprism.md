---
title: "PhotoPrism"
description: "AI-powered photo management with automatic tagging and face recognition"
---

# PhotoPrism

AI-powered photo management with automatic tagging and face recognition

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/self-hosted" class="tag-badge">self-hosted</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/photoprism/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/photoprism/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/photoprism/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `photoprism` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `fd24999ef23a6386ebe32c7dd1c1b70a55f6eb5ab91cd5c3d7ba84e464b45e4f` |

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

   Open [http://localhost:2342](http://localhost:2342) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

