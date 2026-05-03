---
title: "Joern"
description: "Open-source code analysis platform — generate code property graphs from source code and query them for vulnerabilities, dependencies, control flow, and data flow across multiple languages"
---

# Joern

Open-source code analysis platform — generate code property graphs from source code and query them for vulnerabilities, dependencies, control flow, and data flow across multiple languages

## Tags

<a href="/categories/security" class="tag-badge">security</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/joern/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/joern/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/joern/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `joern` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `06cc1f961b6615419f6a18092b2ed26de76e2271cd18fbbf20b799d5f81925aa` |

## Quick Start

1. **Start the Joern server:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify the server is running:**

   ```bash
   curl http://localhost:8080/health
   ```

3. **Import source code for analysis:**

   ```bash
   curl -X POST http://localhost:8080/import \
     -H "Content-Type: application/json" \
     -d '{"path": "/app/source-code"}'
   ```

4. **Run queries via the REST API:**

   ```bash
   curl -X POST http://localhost:8080/run \
     -H "Content-Type: application/json" \
     -d '{"query": "cpg.method.name(\"main\").toJsonPretty()"}'
   ```

   Or use the Joern CLI:

   ```bash
   docker compose exec joern joern
   joern> importCpg("project/cpg.bin")
   joern> cpg.method.name("exec").callIn.where(_.argument.size > 1).l
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Optional Variables

| Variable       | Default    | Description                                        |
|----------------|------------|----------------------------------------------------|
| `JOERN_SERVER` | `true`     | Run in server mode (`true`) or CLI mode (`false`)  |
| `JOERN_PORT`   | `8080`     | Port for the REST API server                       |
| `JOERN_OPTS`   | `-Xmx4G`   | JVM memory and options                             |

## Troubleshooting

| Symptom                                    | Likely Cause         | Fix                                          |
|--------------------------------------------|----------------------|----------------------------------------------|
| Server starts but queries timeout          | JVM heap too small   | Increase `JOERN_OPTS` to `-Xmx8G` or higher   |
| `OutOfMemoryError`                         | Codebase too large   | Reduce the imported codebase or increase heap |
| `Connection refused` on port 8080          | Server still starting| Joern's JVM startup takes 10-30s — check logs |
| Query returns no results                   | CPG not imported     | Import source code first via `/import`        |

## API Endpoints

When running in server mode (`JOERN_SERVER=true`), Joern exposes:

| Endpoint    | Method | Description                          |
|-------------|--------|--------------------------------------|
| `/health`   | GET    | Health check                         |
| `/import`   | POST   | Import source code into a CPG        |
| `/run`      | POST   | Execute a Joern query                |
| `/projects` | GET    | List imported projects               |

### Query Examples

**Find all method definitions:**

```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{"query": "cpg.method.toJsonPretty()"}'
```

**Find all `exec` / `shell` calls (potential command injection):**

```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{"query": "cpg.method.name(\"exec|shell|system|popen\").callIn.where(_.argument.size > 1).l"}'
```

**Map data flow from user input to sink:**

```bash
curl -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{"query": "cpg.method.name(\"exec\").callIn.reachableBy(cpg.method.name(\"read|recv|param\").parameter).l"}'
```

## Health Check

```bash
curl http://localhost:8080/health
```

A healthy server responds with:
```json
{"status": "ok", "version": "2.x.x"}
```

