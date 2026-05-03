---
title: "TypeSense"
description: "Open-source, typo-tolerant search engine — blazing fast full-text search with typo correction, faceted filtering, geosearch, and instant response times under 50ms"
---

# TypeSense

Open-source, typo-tolerant search engine — blazing fast full-text search with typo correction, faceted filtering, geosearch, and instant response times under 50ms

## Tags

<a href="/categories/search" class="tag-badge">search</a> <a href="/categories/database" class="tag-badge">database</a> <a href="/categories/api" class="tag-badge">api</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/typesense/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/typesense/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/typesense/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `typesense` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `b7815811899c59a4d5ee80879a46e75ec37a40af6526ea988ff30d6bbf332c06` |

## Quick Start

1. **Set your API key and start the server:**

   ```bash
   cp .env.example .env
   # Edit .env — set TYPESENSE_API_KEY to a strong random string
   docker compose up -d
   ```

2. **Verify the server is running:**

   ```bash
   curl -X GET http://localhost:8108/health \
     -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}"
   ```

   Expected response: `{"ok": true}`

3. **Create a collection (index):**

   ```bash
   curl -X POST http://localhost:8108/collections \
     -H "Content-Type: application/json" \
     -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}" \
     -d '{
       "name": "books",
       "fields": [
         {"name": "title", "type": "string"},
         {"name": "author", "type": "string"},
         {"name": "year", "type": "int32"},
         {"name": "rating", "type": "float"}
       ],
       "default_sorting_field": "year"
     }'
   ```

4. **Index some documents:**

   ```bash
   curl -X POST http://localhost:8108/collections/books/documents \
     -H "Content-Type: application/json" \
     -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}" \
     -d '{
       "title": "The Great Gatsby",
       "author": "F. Scott Fitzgerald",
       "year": 1925,
       "rating": 4.5
     }'
   ```

5. **Search with typo tolerance:**

   ```bash
   curl "http://localhost:8108/collections/books/documents/search?q=gatsby&query_by=title&per_page=5" \
     -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}"
   ```

   Try a deliberate typo — `gastsby` — and TypeSense will still find "The Great Gatsby".

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable             | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `TYPESENSE_API_KEY`  | API key authenticating all requests. Generate with `openssl rand -hex 32`.  |

### Optional Variables

| Variable               | Default | Description                                  |
|------------------------|---------|----------------------------------------------|
| `TYPESENSE_PORT`       | `8108`  | Host port for the TypeSense API              |
| `TYPESENSE_ENABLE_CORS`| `true`  | Allow browser-based requests                 |

## Troubleshooting

| Symptom                                               | Likely Cause                        | Fix                                                 |
|-------------------------------------------------------|-------------------------------------|-----------------------------------------------------|
| `401 Unauthorized`                                    | Missing or incorrect API key        | Verify `TYPESENSE_API_KEY` in `.env` matches the header value |
| `{"ok": false}` from health endpoint                  | Server not fully initialized        | Wait a few seconds and retry                        |
| Search returns no results                             | Documents not indexed yet           | Check document count: `GET /collections/:name`      |
| Slow import performance                               | Importing one document at a time    | Use the bulk import endpoint with JSON lines         |
| `413 Request Entity Too Large`                        | Document exceeds size limit         | Reduce document size or batch smaller chunks        |

## API Endpoints

TypeSense exposes a REST API on port 8108:

| Endpoint                                    | Method | Description                          |
|---------------------------------------------|--------|--------------------------------------|
| `/health`                                   | GET    | Health check                         |
| `/collections`                              | GET    | List all collections                 |
| `/collections`                              | POST   | Create a collection                  |
| `/collections/:name`                        | GET    | Retrieve a collection                |
| `/collections/:name`                        | DELETE | Drop a collection                    |
| `/collections/:name/documents`              | POST   | Index a document                     |
| `/collections/:name/documents/search`       | GET    | Search documents                     |
| `/collections/:name/documents/:id`          | GET    | Retrieve a document                  |
| `/collections/:name/documents/:id`          | DELETE | Delete a document                    |
| `/collections/:name/documents/export`       | GET    | Export all documents as JSON lines   |
| `/collections/:name/documents/import`       | POST   | Bulk import documents (JSON lines)   |
| `/multi_search`                             | POST   | Search multiple collections at once  |

Full API reference: [typesense.org/docs/latest/api](https://typesense.org/docs/latest/api/)

## Health Check

```bash
curl -X GET http://localhost:8108/health \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}"
```

A healthy server returns:
```json
{"ok": true}
```

