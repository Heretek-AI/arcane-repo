---
title: "NanoBot"
description: "Lightweight AI chatbot framework with tool calling and multi-provider support"
---

# NanoBot

Lightweight AI chatbot framework with tool calling and multi-provider support

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/framework" class="tag-badge">framework</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nanobot/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nanobot/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/nanobot/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `nanobot` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `530ee581ec53ebc39a7aaa946b140394a6e4f49236dfc6144fc2c84483143ab5` |

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

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

> **Status: 🏗️ CI Build Pending**
> The upstream project includes a Dockerfile, but no pre-built image is published. The template currently
> references a non-existent image. A CI pipeline will build and publish to GHCR (planned for future update).

