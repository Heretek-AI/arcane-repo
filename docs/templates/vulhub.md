---
title: "Vulhub"
description: "Pre-built vulnerable environments collection — ~200 compose-based CVE labs for security training and exploit development"
---

# Vulhub

Pre-built vulnerable environments collection — ~200 compose-based CVE labs for security training and exploit development

## Tags

<a href="/categories/security" class="tag-badge">security</a> <a href="/categories/non-serviceable" class="tag-badge">non-serviceable</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vulhub/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vulhub/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/vulhub/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `vulhub` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8651626d497051921ae28d7f144530e238e9cb1eb6bdf31fd20f7470214eef50` |

## Quick Start

1. **Start the informational wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **Browse available CVEs:**

   ```bash
   curl http://localhost:8000/categories | python -m json.tool
   ```

## Configuration

| Variable        | Default  | Description                         |
|-----------------|----------|-------------------------------------|
| `VULHUB_PORT`   | `8000`   | Host port for the info API          |

## Troubleshooting

| Symptom                            | Likely Cause                | Fix                                                              |
|------------------------------------|-----------------------------|------------------------------------------------------------------|
| No vulnerable labs available       | This is a reference stub    | `git clone https://github.com/vulhub/vulhub` for real labs       |
| Container exits immediately        | pip install failure         | Run `docker compose logs vulhub` for details                     |
| Can't find a specific CVE          | Not in this container       | Browse `https://github.com/vulhub/vulhub` for the full catalog   |
| Port conflict for specific CVE lab | Port already used           | Vulhub labs use unique ports; check `lsof -i :<port>` first      |

## API Endpoints

| Endpoint      | Method | Description                                      |
|---------------|--------|--------------------------------------------------|
| `/health`     | GET    | Health check — confirms the info stub is running |
| `/guide`      | GET    | Usage instructions and catalog overview          |
| `/categories` | GET    | Top CVEs and full catalog link                   |

