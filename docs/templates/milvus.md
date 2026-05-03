---
title: "Milvus"
description: "Open-source vector database built for scalable similarity search — manage billion-scale vector datasets with GPU-accelerated indexing, hybrid search, and multi-language SDKs"
---

# Milvus

Open-source vector database built for scalable similarity search — manage billion-scale vector datasets with GPU-accelerated indexing, hybrid search, and multi-language SDKs

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/search" class="tag-badge">search</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/milvus/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/milvus/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/milvus/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `milvus` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `0f1217e31241104c4e0bbac4ec1caa569943106183a6b8af0685459314de168b` |

## Quick Start

1. **Start the stack:**

   ```bash
   docker compose up -d
   ```

2. **Verify all services are healthy:**

   ```bash
   docker compose ps
   ```

   All three services (milvus, etcd, minio) should show `Up` status.

3. **Connect using the Python SDK:**

   ```bash
   pip install pymilvus
   ```

   ```python
   from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType

   # Connect to the Milvus server
   connections.connect(host="localhost", port="19530")

   # Create a collection
   schema = CollectionSchema([
       FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
       FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=128),
       FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=512),
   ])
   collection = Collection(name="documents", schema=schema)
   print(f"Created collection: {collection.name}")
   ```

4. **Insert vectors and search:**

   ```python
   import random

   # Insert sample data
   vectors = [[random.random() for _ in range(128)] for _ in range(10)]
   ids = list(range(10))
   texts = [f"document_{i}" for i in range(10)]
   collection.insert([ids, vectors, texts])

   # Build an index
   index_params = {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}}
   collection.create_index("embedding", index_params)

   # Search
   search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
   results = collection.search(
       data=[vectors[0]],  # query vector
       anns_field="embedding",
       param=search_params,
       limit=3
   )
   for hit in results[0]:
       print(f"ID: {hit.id}, Distance: {hit.distance}")
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Milvus

| Variable       | Default  | Description                               |
|----------------|----------|-------------------------------------------|
| `MILVUS_PORT`  | `19530`  | Host port for the Milvus gRPC API         |

### ETCD (Metadata Store)

| Variable           | Default           | Description                              |
|--------------------|-------------------|------------------------------------------|
| `ETCD_PORT`        | `2379`            | Host port for etcd client API            |
| `ETCD_ENDPOINTS`   | `milvus-etcd:2379`| ETCD endpoint(s) for Milvus to connect to |

### MinIO (Object Storage)

| Variable              | Default       | Description                              |
|-----------------------|---------------|------------------------------------------|
| `MINIO_PORT`          | `9000`        | Host port for MinIO S3 API               |
| `MINIO_CONSOLE_PORT`  | `9001`        | Host port for MinIO web console          |
| `MINIO_ROOT_USER`     | `minioadmin`  | MinIO access key / username              |
| `MINIO_ROOT_PASSWORD` | `minioadmin`  | MinIO secret key / password              |
| `MINIO_ADDRESS`       | `milvus-minio:9000` | MinIO address for Milvus to connect to |

## Troubleshooting

| Symptom                                                | Likely Cause                     | Fix                                                |
|--------------------------------------------------------|----------------------------------|----------------------------------------------------|
| Milvus fails to start                                 | ETCD or MinIO not ready          | Check `docker compose ps` — wait for all services  |
| `fail to connect to server`                            | Milvus not fully started         | Wait 10–15 seconds for initial startup             |
| Write operations slow                                  | MinIO credentials mismatch        | Verify `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` match across services |
| Connection refused on port 2379                        | ETCD still starting               | Check logs: `docker compose logs etcd`             |
| `grpc: the connection is unavailable`                  | Client-server incompatibility     | Ensure your client SDK version matches the server version |

## Health Check

```bash
# Check all service status
docker compose ps

# Direct Milvus health check
curl -X GET http://localhost:19530/health

# Check MinIO health
curl http://localhost:9000/minio/health/live
```

