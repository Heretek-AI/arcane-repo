# CompreFace — Face Recognition System

[CompreFace](https://github.com/exadel-inc/CompreFace) is the leading free open-source face recognition system. It provides a REST API for face detection, recognition, verification, and landmark detection.

## Quick Start

1. **Start the services:**

   ```bash
   docker compose up -d
   ```

2. **Wait for initialization** (may take 1-2 minutes on first start for the database to initialize and the API to create tables).

3. **Check the API is ready:**

   ```bash
   curl http://localhost:8000/api/v1/status
   ```

4. **Create a face recognition service** via the API:

   ```bash
   curl -X POST http://localhost:8000/api/v1/recognition/faces \
     -H "Content-Type: application/json" \
     -d '{
       "name": "My Service",
       "subject": "User"
     }'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                  | Default       | Description                                |
|---------------------------|---------------|--------------------------------------------|
| `COMPREFACE_PORT`         | `8000`        | Host port for the API                      |
| `COMPREFACE_DB`           | `compreface`  | PostgreSQL database name                   |
| `COMPREFACE_DB_USER`      | `compreface`  | PostgreSQL user                            |
| `COMPREFACE_DB_PASSWORD`  | `changeme`    | PostgreSQL password — **change for prod**  |
| `COMPREFACE_JAVA_OPTS`    | `-Xms512m -Xmx2g` | Java heap memory settings           |

## Architecture

This template provides a simplified core setup:

- **compreface-api**: The main REST API service exposing face recognition endpoints
- **compreface-db**: PostgreSQL database for storing face data and service configurations

The upstream project also includes a UI dashboard and admin panel — add those services from the [official docker-compose](https://github.com/exadel-inc/CompreFace/blob/master/docker-compose.yml) if needed.

## API Features

- **Face Detection**: Locate faces in images
- **Face Recognition**: Match faces against a database of known subjects
- **Face Verification**: Verify if two faces belong to the same person
- **Landmark Detection**: Detect facial landmarks (eyes, nose, mouth)
- **Age & Gender**: Estimate age and gender from face images
- **Mask Detection**: Detect whether a face is wearing a mask

## Adding Faces

Add an example face to a subject:

```bash
curl -X POST "http://localhost:8000/api/v1/recognition/faces?subject=User" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/face.jpg" \
  -F "det_prob_threshold=0.8"
```

## Health Check

```bash
curl http://localhost:8000/api/v1/status
```

Full documentation: [github.com/exadel-inc/CompreFace](https://github.com/exadel-inc/CompreFace)
