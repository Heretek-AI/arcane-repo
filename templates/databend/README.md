# Databend — Cloud Data Warehouse

[Databend](https://databend.com) is an open-source cloud data warehouse. It provides fast, elastic SQL analytics on object storage with MySQL wire-compatible protocol, real-time columnar performance, and instant scaling.

## Quick Start

1. **Start the server:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Connect using the MySQL client:**

   ```bash
   mysql -h 127.0.0.1 -P 8000 -u root
   ```

3. **Run a query:**

   ```sql
   SELECT 'Hello, Databend!' AS greeting;
   ```

4. **Create a table and insert data:**

   ```sql
   CREATE TABLE IF NOT EXISTS books (
       id INT,
       title VARCHAR,
       author VARCHAR,
       year INT
   );

   INSERT INTO books VALUES
       (1, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925),
       (2, 'To Kill a Mockingbird', 'Harper Lee', 1960);

   SELECT * FROM books WHERE year > 1950;
   ```

5. **Use the HTTP handler (REST API):**

   ```bash
   curl -X POST http://localhost:8124/v1/query \
     -H "Content-Type: application/json" \
     -d '{"sql": "SELECT * FROM books"}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Optional Variables

| Variable                | Default  | Description                                                   |
|-------------------------|----------|---------------------------------------------------------------|
| `DATABEND_PORT`         | `8000`   | MySQL wire protocol port                                      |
| `DATABEND_HTTP_PORT`    | `8124`   | HTTP handler (REST query) port                                |
| `DATABEND_MINIO_PORT`   | `9000`   | Embedded MinIO port (when MINIO_ENABLED=true)                 |
| `QUERY_DEFAULT_USER`    | `root`   | Default SQL user                                              |
| `QUERY_DEFAULT_PASSWORD`| (empty)  | Default SQL password                                          |
| `QUERY_STORAGE_TYPE`    | `fs`     | Storage backend: `fs` (local) or `s3`                         |
| `MINIO_ENABLED`         | `false`  | Enable built-in MinIO for local S3-compatible object storage  |

## API Endpoints

Databend exposes both MySQL-compatible and REST interfaces:

| Interface     | Port  | Protocol        | Description                        |
|---------------|-------|-----------------|------------------------------------|
| MySQL Handler | 8000  | MySQL wire      | Connect with any MySQL client      |
| HTTP Handler  | 8124  | HTTP REST       | SQL queries via JSON API           |
| MinIO (opt)   | 9000  | S3-compatible   | Built-in object storage (MinIO)    |

### REST API Example

```bash
curl -X POST http://localhost:8124/v1/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT database(), version()"}'
```

## Health Check

**MySQL handler health:**

```bash
mysql -h 127.0.0.1 -P 8000 -u root -e "SELECT 1"
```

**HTTP handler health:**

```bash
curl -s -X POST http://localhost:8124/v1/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT 1"}' | grep -q "1" && echo "healthy"
```

A healthy server responds with query results on either interface.

## Managing Databend

**View logs:**

```bash
docker compose logs -f databend
```

**Access the Meta service (embedded):**

Databend's all-in-one image includes both the query layer and an embedded meta service. For production, consider deploying separate `databend-query` and `databend-meta` containers with a shared MinIO/S3 backend.

**Reset data:**

```bash
docker compose down -v
docker compose up -d
```

**Bulk load CSV data:**

```bash
curl -X PUT http://localhost:8000/v1/streaming_load \
  -H "insert_sql: INSERT INTO books FILE_FORMAT = (type = CSV)" \
  -F "upload=@/path/to/books.csv"
```

## Troubleshooting

| Symptom                                             | Likely Cause                     | Fix                                                      |
|-----------------------------------------------------|----------------------------------|----------------------------------------------------------|
| `ERROR 2013 (HY000): Lost connection`               | Server not ready                 | Wait a few seconds and retry                             |
| `Access denied for user`                            | Wrong credentials                | Verify `QUERY_DEFAULT_USER` and `QUERY_DEFAULT_PASSWORD` |
| Query returns no results                            | Table or database doesn't exist  | Create the database first with `CREATE DATABASE`         |
| `No handler for protocol`                           | Wrong port                       | Use port 8000 (MySQL) or 8124 (HTTP)                     |
