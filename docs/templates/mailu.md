---
title: "Mailu"
description: "Mailu mail server — lightweight email server with webmail, admin UI, and anti-spam. No public Docker images found on Docker Hub; this template provides an informational API stub"
---

# Mailu

Mailu mail server — lightweight email server with webmail, admin UI, and anti-spam. No public Docker images found on Docker Hub; this template provides an informational API stub

## Tags

<a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mailu/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mailu/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/mailu/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `mailu` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `324cb0c46729337ba67db9074645e8c421390f94dd1a168bb4331b15baa6ad21` |

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

| Variable      | Default  | Description                       |
|---------------|----------|-----------------------------------|
| `MAILU_PORT`  | `8000`   | Host port for the informational API stub |

## Troubleshooting

| Symptom                          | Likely Cause              | Fix                                                              |
|----------------------------------|---------------------------|------------------------------------------------------------------|
| No mail server functionality     | This is a Docker stub     | Use the official setup wizard at setup.mailu.io                  |
| Container exits immediately      | pip install failure       | Run `docker compose logs mailu` for details                      |
| Need full email stack            | Using wrong deployment    | Mailu provides its own compose config generator — use it         |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + missing-image info                    |
| `/guide`  | GET    | Official setup wizard and source-build instructions   |

