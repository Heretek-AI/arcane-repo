---
title: "Onyx"
description: "Enterprise AI search platform for connecting, indexing, and searching organizational knowledge — formerly Danswer"
---

# Onyx

Enterprise AI search platform for connecting, indexing, and searching organizational knowledge — formerly Danswer

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/search" class="tag-badge">search</a> <a href="/categories/rag" class="tag-badge">rag</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/onyx/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/onyx/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/onyx/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `onyx` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `faf5bb968c1c64ba5754d0f04f62df64e3df9296a5f7b67c3c7df2f3a99d7f58` |

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

