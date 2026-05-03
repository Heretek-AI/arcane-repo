# Stirling Pdf

Self-hosted PDF manipulation toolkit for merging, splitting, converting, OCR, and watermarking documents

This template provides a containerized deployment of [Stirling Pdf](https://github.com/stirlingtools/stirling-pdf) using Docker Compose.

## Quick Start

1. **Clone and configure:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Verify it's running:**

   ```bash
   docker compose ps
   curl -s http://localhost:8080/ | head -c 200
   ```

4. **Access the application:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Architecture

| Component | Image | Purpose |
|-----------|-------|---------|
| `stirling-pdf` | docker.io/stirlingtools/stirling-pdf:latest | Main application service |
| `stirling-pdf_data` | (volume) | Persistent data storage |

Services communicate over a shared Docker network. Data is persisted in named volumes.

## Configuration

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `STIRLING_PDF_PORT` | `8080` | Configuration variable |


## Troubleshooting

**Container won't start:**
```bash
docker compose logs stirling-pdf
```

**Port conflict:**
Edit `.env` and change `STIRLING-PDF_PORT` to an available port, then restart:
```bash
docker compose down && docker compose up -d
```

**Permission errors:**
Ensure the Docker user has write access to the data volume:
```bash
docker compose exec stirling-pdf ls -la /data
```

**Health check failing:**
```bash
docker compose ps  # Check STATUS column
docker inspect stirling-pdf --format='{{json .State.Health}}'
```

## Backup & Recovery

**Backup:**
```bash
# Stop the service
docker compose down

# Backup the data volume
docker run --rm -v stirling-pdf_data:/data -v $(pwd):/backup alpine tar czf /backup/stirling-pdf-backup-$(date +%Y%m%d).tar.gz /data

# Restart
docker compose up -d
```

**Restore:**
```bash
docker compose down
docker run --rm -v stirling-pdf_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar xzf /backup/stirling-pdf-backup.tar.gz -C /"
docker compose up -d
```

## Links

- **Project Homepage:** [Stirling Pdf](https://github.com/stirlingtools/stirling-pdf)
- **Docker Image:** `docker.io/stirlingtools/stirling-pdf:latest`
- **Documentation:** [GitHub Wiki](https://github.com/stirlingtools/stirling-pdf/wiki)
- **Issues:** [GitHub Issues](https://github.com/stirlingtools/stirling-pdf/issues)


## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+
- 512MB+ RAM recommended
- 1GB+ free disk space for data storage
