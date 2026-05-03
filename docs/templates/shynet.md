---
title: "Shynet"
description: "Shynet web analytics — privacy-friendly, cookie-free analytics. No Docker image or upstream Dockerfile exists; this template provides an informational API stub"
---

# Shynet

Shynet web analytics — privacy-friendly, cookie-free analytics. No Docker image or upstream Dockerfile exists; this template provides an informational API stub

## Tags

<a href="/categories/analytics" class="tag-badge">analytics</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shynet/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shynet/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/shynet/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `shynet` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `dd8fc59ca6acf9c65473f0cdfc172606e3479a45ba8869c8cb8fb75044d7c20a` |

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Configuration

| Variable       | Default  | Description                       |
|----------------|----------|-----------------------------------|
| `SHYNET_PORT`  | `8000`   | Host port for the informational API stub |

## Troubleshooting

| Symptom                          | Likely Cause              | Fix                                                              |
|----------------------------------|---------------------------|------------------------------------------------------------------|
| No analytics functionality       | This is a Docker stub     | Clone and deploy Shynet as a Django app with PostgreSQL          |
| Container exits immediately      | pip install failure       | Run `docker compose logs shynet` for details                     |
| Need analytics dashboard         | Using wrong deployment    | Shynet is a Django project — deploy with gunicorn + PostgreSQL   |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + missing-Dockerfile info               |
| `/guide`  | GET    | Django application deployment instructions             |

