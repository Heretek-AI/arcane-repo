---
title: "Vane"
description: "Visual AI agent builder with drag-and-drop canvas"
---

# Vane

Visual AI agent builder with drag-and-drop canvas

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/low-code" class="tag-badge">low-code</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vane/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vane/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vane/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `vane` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `9a6a9e1776844767748da749f7442a5251186c72f889e013b3100d50c42550b1` |

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

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.

> **Status: 🏗️ CI Build Pending**
> The upstream project includes a Dockerfile, but no pre-built image is published. The template currently
> references a non-existent image. A CI pipeline will build and publish to GHCR (planned for future update).

