---
title: "LangGraph-Swarm"
description: "Python swarm intelligence for multi-LLM agent coordination"
---

# LangGraph-Swarm

Python swarm intelligence for multi-LLM agent coordination

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/agents" class="tag-badge">agents</a> <a href="/categories/python" class="tag-badge">python</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langgraphswarm/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langgraphswarm/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/langgraphswarm/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `langgraphswarm` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8289bb0e46ed7bba1295839f7e142f9bb95aed97e14256e1c4a7ec719403bf18` |

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

