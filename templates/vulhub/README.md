# Vulhub — Pre-Built Vulnerable Environments by Docker Compose

> **Reference catalog — not a deployable Docker service.**
> [Vulhub](https://github.com/vulhub/vulhub) is a collection of ~200
> CVE-specific vulnerable environment Docker Compose files for security
> training, exploit development, and blue-team exercises.
> This Docker template provides a minimal informational API that indexes
> the upstream catalog. Clone the upstream repo for working environments.

## Quick Start (Info API)

1. **Start the informational wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **Browse available CVEs:**

   ```bash
   curl http://localhost:8000/categories | python -m json.tool
   ```

## Full Usage (Recommended) — Clone the Upstream Repo

Vulhub is a directory of per-CVE Docker Compose files. Each CVE has its own
self-contained compose setup:

```bash
git clone https://github.com/vulhub/vulhub
cd vulhub

# Pick any CVE, e.g. Log4Shell:
cd log4j/CVE-2021-44228
docker compose up -d

# The vulnerable service is now running — exploit it, capture evidence,
# then tear down:
docker compose down -v
```

### Popular Labs

| CVE              | Name                              | Path                           |
|------------------|-----------------------------------|--------------------------------|
| CVE-2021-44228   | Log4Shell (Log4j RCE)             | `log4j/CVE-2021-44228`        |
| CVE-2017-5638    | Apache Struts2 Remote Code Exec   | `struts2/s2-045`              |
| CVE-2021-41773   | Apache HTTPD Path Traversal       | `httpd/CVE-2021-41773`        |
| CVE-2022-22965   | Spring4Shell                      | `spring/CVE-2022-22965`       |
| CVE-2019-9193    | PostgreSQL COPY FROM PROGRAM RCE  | `postgres/CVE-2019-9193`      |

Over 200 environments available — web apps, databases, CMS, network services,
programming frameworks, and OS-level CVEs.

## Configuration

| Variable        | Default  | Description                         |
|-----------------|----------|-------------------------------------|
| `VULHUB_PORT`   | `8000`   | Host port for the info API          |

## API Endpoints

| Endpoint      | Method | Description                                      |
|---------------|--------|--------------------------------------------------|
| `/health`     | GET    | Health check — confirms the info stub is running |
| `/guide`      | GET    | Usage instructions and catalog overview          |
| `/categories` | GET    | Top CVEs and full catalog link                   |

## Managing

**View logs:**

```bash
docker compose logs -f vulhub
```

## Troubleshooting

| Symptom                            | Likely Cause                | Fix                                                              |
|------------------------------------|-----------------------------|------------------------------------------------------------------|
| No vulnerable labs available       | This is a reference stub    | `git clone https://github.com/vulhub/vulhub` for real labs       |
| Container exits immediately        | pip install failure         | Run `docker compose logs vulhub` for details                     |
| Can't find a specific CVE          | Not in this container       | Browse `https://github.com/vulhub/vulhub` for the full catalog   |
| Port conflict for specific CVE lab | Port already used           | Vulhub labs use unique ports; check `lsof -i :<port>` first      |
