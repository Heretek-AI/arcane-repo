# Stirling-PDF — Self-Hosted PDF Toolkit

[Stirling-PDF](https://github.com/Stirling-Tools/Stirling-PDF) is a self-hosted web application for manipulating PDF files. It supports merging, splitting, converting, OCR, watermarking, rotating, compressing, and dozens of other PDF operations — all running locally with no data leaving your server.

**Who it's for:** Anyone who regularly works with PDFs and wants a privacy-first, self-hosted alternative to online PDF tools. Runs entirely on your infrastructure with no cloud dependencies or usage limits.

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the UI:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Architecture

This is a single-service template with no external database or cache dependencies.

| Component | Details |
|-----------|---------|
| **Image** | `stirlingtools/stirling-pdf:latest` |
| **Port** | `8080` (configurable via `STIRLING_PDF_PORT`) |
| **Volume** | `stirling-pdf_data` → `/data` (temporary file processing, config) |
| **Restart** | `unless-stopped` |
| **Health check** | HTTP probe on `http://localhost:8080/` every 30s |

All PDF processing happens inside the container. Uploaded files are stored temporarily in the `/data` volume and are not persisted long-term — they're cleaned up after processing.

## Configuration Reference

Copy `.env.example` to `.env` and adjust values as needed.

| Variable | Default | Description |
|----------|---------|-------------|
| `STIRLING_PDF_PORT` | `8080` | Host port for the Stirling-PDF web interface |

### Additional Environment Variables

Stirling-PDF supports many optional environment variables for advanced configuration. These are set in the container environment — add them to your `docker-compose.yml` under `environment:` or to your `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECURITY_ENABLE_LOGIN` | `false` | Enable username/password authentication |
| `SECURITY_INITIAL_LOGIN_USERNAME` | `admin` | Default admin username (only used on first startup) |
| `SECURITY_INITIAL_LOGIN_PASSWORD` | `stirling` | Default admin password (only used on first startup) |
| `SYSTEM_DEFAULTLOCALE` | `en-US` | UI language locale |
| `SYSTEM_MAXFILESIZE` | `100` | Maximum upload file size in MB |
| `SYSTEM_MAXTHREADS` | `unset` | Max threads for PDF processing (defaults to CPU cores) |
| `UI_APPNAME` | `Stirling-PDF` | Custom app name shown in the UI |
| `UI_HOMEDESCRIPTION` | _built-in_ | Custom description on the home page |
| `UI_APPNAMENAVBAR` | _built-in_ | Custom navbar title |
| `ENDPOINTS_TO_REMOVE` | _none_ | Comma-separated list of endpoints to hide from the UI |
| `ENDPOINTS_GROUPSTOREMOVE` | _none_ | Comma-separated groups to hide (e.g., `Image,Pipeline`) |

For the full list, see the [Stirling-PDF configuration reference](https://github.com/Stirling-Tools/Stirling-PDF/blob/main/README.md).

### Enabling Authentication

To password-protect the interface:

```bash
# In your .env file
SECURITY_ENABLE_LOGIN=true
SECURITY_INITIAL_LOGIN_USERNAME=admin
SECURITY_INITIAL_LOGIN_PASSWORD=changeme
```

Restart the container after changing these values:

```bash
docker compose up -d
```

## Key Features

- **Merge** multiple PDFs into one
- **Split** PDFs by page range or into individual pages
- **Convert** to/from PDF (images, Word, HTML, Markdown, and more)
- **OCR** — add text layer to scanned documents
- **Rotate**, **crop**, **resize** pages
- **Watermark** with text or images
- **Compress** PDFs to reduce file size
- **Encrypt/decrypt** password-protected PDFs
- **Sign** PDFs with digital signatures
- **Repair** corrupted PDF files
- **Add/remove** metadata
- **Multi-page layout** — arrange multiple pages per sheet
- **Pipeline** — chain multiple operations together

## Troubleshooting

**Container won't start / health check fails:**

Check logs for errors:
```bash
docker compose logs stirling-pdf
```

Verify the port isn't already in use:
```bash
lsof -i :8080
# or change the port in .env
STIRLING_PDF_PORT=9090
```

**"File too large" errors:**

Increase the max file size limit:
```bash
# In .env
SYSTEM_MAXFILESIZE=500
```
Restart the container after changing.

**Slow PDF processing:**

Stirling-PDF uses OCRmyPDF for OCR operations, which can be CPU-intensive. For large scanned documents:
- Increase `SYSTEM_MAXTHREADS` if you have spare CPU cores
- Consider allocating more memory to the container via `docker-compose.yml`:
  ```yaml
  deploy:
    resources:
      limits:
        memory: 4G
  ```

**UI not loading after enabling login:**

If you set login credentials after first startup, the initial credentials may not apply. Reset by clearing the volume data or using the password reset procedure in the [Stirling-PDF docs](https://github.com/Stirling-Tools/Stirling-PDF).

## Backup & Recovery

Stirling-PDF is stateless by default — uploaded files are temporary and cleaned up after processing. The only persistent data in the volume is configuration and (if enabled) user accounts.

**Backup:**

```bash
# Stop the container to ensure data consistency
docker compose stop stirling-pdf

# Back up the volume
docker run --rm -v stirling-pdf_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/stirling-pdf-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restart
docker compose start stirling-pdf
```

**Restore:**

```bash
docker compose stop stirling-pdf

docker run --rm -v stirling-pdf_data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/stirling-pdf-backup-YYYYMMDD.tar.gz -C /data

docker compose start stirling-pdf
```

**Rebuild from scratch (no backup needed):**

If you don't use authentication, you can safely destroy and recreate the volume with no data loss since all processing is ephemeral:
```bash
docker compose down -v
docker compose up -d
```

## Links

- **Original Project:** [github.com/Stirling-Tools/Stirling-PDF](https://github.com/Stirling-Tools/Stirling-PDF)
- **Docker Hub:** [hub.docker.com/r/stirlingtools/stirling-pdf](https://hub.docker.com/r/stirlingtools/stirling-pdf)
- **Documentation:** [github.com/Stirling-Tools/Stirling-PDF/wiki](https://github.com/Stirling-Tools/Stirling-PDF/wiki)
- **Community / Support:** [github.com/Stirling-Tools/Stirling-PDF/issues](https://github.com/Stirling-Tools/Stirling-PDF/issues)
