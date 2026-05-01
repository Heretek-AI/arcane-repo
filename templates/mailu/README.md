# Mailu — Lightweight Mail Server

> **No public Docker images — use the official setup wizard.**
> [Mailu](https://mailu.io) is a lightweight yet complete mail server suite
> with webmail (Roundcube), admin UI, anti-spam (Rspamd), and antivirus
> (ClamAV). No public Docker images were found on Docker Hub (the `mailu/`
> namespace returned 404). This Docker template provides a minimal
> informational API stub. Use the official setup wizard at
> [setup.mailu.io](https://setup.mailu.io) for the full deployment.

## Quick Start

1. **Start the informational API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

## Full Installation (Recommended)

Use Mailu's official setup wizard to generate a docker-compose configuration:

1. Visit [setup.mailu.io](https://setup.mailu.io)
2. Fill in your domain, hostname, and feature preferences
3. Download the generated `docker-compose.yml` and `.env`
4. Run `docker compose up -d`

Or clone and build from source:

```bash
git clone https://github.com/Mailu/Mailu
cd Mailu
docker compose up -d
```

## Configuration

| Variable      | Default  | Description                       |
|---------------|----------|-----------------------------------|
| `MAILU_PORT`  | `8000`   | Host port for the informational API stub |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + missing-image info                    |
| `/guide`  | GET    | Official setup wizard and source-build instructions   |

## Managing

**View logs:**

```bash
docker compose logs -f mailu
```

## Troubleshooting

| Symptom                          | Likely Cause              | Fix                                                              |
|----------------------------------|---------------------------|------------------------------------------------------------------|
| No mail server functionality     | This is a Docker stub     | Use the official setup wizard at setup.mailu.io                  |
| Container exits immediately      | pip install failure       | Run `docker compose logs mailu` for details                      |
| Need full email stack            | Using wrong deployment    | Mailu provides its own compose config generator — use it         |
