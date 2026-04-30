# TypeSense — Typo-Tolerant Search Engine

[TypeSense](https://typesense.org) is an open-source, typo-tolerant search engine. It delivers instant (<50ms) search results with typo correction, faceted filtering, geosearch, vector search, and automatic ranking — all with a simple REST API. Think of it as an open-source alternative to Algolia with a fraction of the infrastructure cost.

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

## Managing TypeSense

**View logs:**

```bash
docker compose logs -f typesense
```

**Bulk import from a JSONL file:**

```bash
curl -X POST http://localhost:8108/collections/books/documents/import \
  -H "Content-Type: text/plain" \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}" \
  --data-binary @books.jsonl
```

**Export all documents:**

```bash
curl http://localhost:8108/collections/books/documents/export \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}" > books-export.jsonl
```

**Check collection statistics:**

```bash
curl http://localhost:8108/collections/books \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY:-your-api-key}"
```

## Troubleshooting

| Symptom                                               | Likely Cause                        | Fix                                                 |
|-------------------------------------------------------|-------------------------------------|-----------------------------------------------------|
| `401 Unauthorized`                                    | Missing or incorrect API key        | Verify `TYPESENSE_API_KEY` in `.env` matches the header value |
| `{"ok": false}` from health endpoint                  | Server not fully initialized        | Wait a few seconds and retry                        |
| Search returns no results                             | Documents not indexed yet           | Check document count: `GET /collections/:name`      |
| Slow import performance                               | Importing one document at a time    | Use the bulk import endpoint with JSON lines         |
| `413 Request Entity Too Large`                        | Document exceeds size limit         | Reduce document size or batch smaller chunks        |
