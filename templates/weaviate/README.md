# Weaviate — Vector Database

[Weaviate](https://weaviate.io) is an open-source vector database that stores both objects and vector embeddings, enabling hybrid search (vector + keyword), similarity search, and generative AI retrieval-augmented generation (RAG) pipelines. This template runs a single Weaviate node with persistent storage and module support for popular embedding providers.

## Quick Start

1. **Start the server:**

   ```bash
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8080/v1/.well-known/ready
   ```

   Expected response: `{"ready": true}`

3. **Create a class (collection) with auto-generated vectors:**

   ```bash
   curl -X POST http://localhost:8080/v1/schema \
     -H "Content-Type: application/json" \
     -d '{
       "class": "Document",
       "description": "A text document",
       "properties": [
         {"name": "content", "dataType": ["text"], "description": "The document content"}
       ]
     }'
   ```

4. **Insert an object:**

   ```bash
   curl -X POST http://localhost:8080/v1/objects \
     -H "Content-Type: application/json" \
     -d '{
       "class": "Document",
       "properties": {
         "content": "Weaviate is an open-source vector database."
       }
     }'
   ```

5. **Search with a vector query:**

   ```bash
   curl -X POST http://localhost:8080/v1/graphql \
     -H "Content-Type: application/json" \
     -d '{
       "query": "{
         Get {
           Document(nearText: {concepts: [\"vector database\"]}) {
             content
           }
         }
       }"
     }'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                                 | Default     | Description                                            |
|------------------------------------------|-------------|--------------------------------------------------------|
| `WEAVIATE_PORT`                          | `8080`      | Host port for the Weaviate API                         |
| `AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED`| `true`      | Allow unauthenticated access                           |
| `CLUSTER_HOSTNAME`                       | `weaviate-node-0` | Node name for multi-node deployments            |
| `DEFAULT_VECTORIZER_MODULE`              | `none`      | Default vectorizer (set to a module for auto-vectorization) |

### Vectorizer Modules

Weaviate supports pluggable vectorizer modules that auto-generate embeddings during import. To enable a specific vectorizer, set `DEFAULT_VECTORIZER_MODULE` and ensure the corresponding API key is available:

| Module                           | API Key Env Var                                                   |
|----------------------------------|-------------------------------------------------------------------|
| `text2vec-openai`                | `OPENAI_APIKEY`                                                   |
| `text2vec-cohere`                | `COHERE_APIKEY`                                                   |
| `text2vec-huggingface`           | `HUGGINGFACE_APIKEY`                                              |
| `text2vec-ollama`                | None (local, but Ollama must be reachable at `OLLAMA_HOST`)       |

Without a vectorizer module, you must provide your own embeddings when inserting objects (e.g., from an external embedding API).

## API Endpoints

Weaviate exposes a REST API and a GraphQL API on port 8080:

| Endpoint                          | Method | Description                                    |
|-----------------------------------|--------|------------------------------------------------|
| `/v1/.well-known/ready`           | GET    | Readiness check                                |
| `/v1/.well-known/live`            | GET    | Liveness check                                 |
| `/v1/schema`                      | GET    | List all classes                               |
| `/v1/schema`                      | POST   | Create a class                                 |
| `/v1/objects`                     | GET    | List objects                                   |
| `/v1/objects`                     | POST   | Create an object                               |
| `/v1/graphql`                     | POST   | GraphQL query (Get, Aggregate, Explore)        |
| `/v1/classification`              | POST   | Start a classification                         |
| `/v1/meta`                        | GET    | Weaviate version and configuration metadata    |

## Health Check

```bash
curl http://localhost:8080/v1/.well-known/ready
```

A ready node returns:
```json
{"ready": true}
```

## Managing Weaviate

**View logs:**

```bash
docker compose logs -f weaviate
```

**Import data from a file (using the REST API):**

```bash
curl -X POST http://localhost:8080/v1/batch/objects \
  -H "Content-Type: application/json" \
  -d '{"objects": [{"class": "Document", "properties": {"content": "First document"}}, {"class": "Document", "properties": {"content": "Second document"}}]}'
```

**Check Weaviate version:**

```bash
curl http://localhost:8080/v1/meta
```

## Troubleshooting

| Symptom                                               | Likely Cause                            | Fix                                                  |
|-------------------------------------------------------|-----------------------------------------|------------------------------------------------------|
| Connection refused on port 8080                       | Container still starting                 | Wait a few seconds and retry                         |
| `{"error":[{"message":"no module with name ..."}]}`   | Vectorizer module not enabled            | Set `ENABLE_MODULES` env var with the module name    |
| 401 Unauthorized                                      | Anonymous access disabled but no key set | Set `AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true` or configure an API key |
| Objects inserted but search returns no results        | No vectorizer and no vectors provided    | Either enable a vectorizer module or supply vectors manually |
