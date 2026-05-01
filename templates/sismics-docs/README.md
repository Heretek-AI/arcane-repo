# Sismics Docs

[Sismics Docs](https://github.com/sismics/docs) — Lightweight self-hosted document management system. Store, organize, tag, and full-text search your documents through a clean web interface with OCR support.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the web UI:**

   Open [http://localhost:8080](http://localhost:8080).

   Create an account on first launch (the first registered user becomes admin).

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

| Variable | Default | Description |
|---|---|---|
| `SISMICS_PORT` | `8080` | Host port for the web UI |
| `SISMICS_BASE_URL` | `http://localhost:8080` | Base URL for accessing the application |

## Service Details

- **Web UI** — Document management interface on port 8080
- **Document Storage** — Upload and organize PDFs, images, and office documents
- **Full-Text Search** — Search across all document content and metadata
- **Tagging** — Organize documents with a flexible tag system
- **OCR** — Optical character recognition for scanned documents
- **Workflows** — Document review and approval workflows
- **Multi-User** — Role-based access control with admin, writer, and reader roles
- **Storage** — All documents and metadata persisted in the `sismics_data` named volume

## Upstream

- [GitHub Repository](https://github.com/sismics/docs)
- [Docker Hub](https://hub.docker.com/r/sismics/docs)
