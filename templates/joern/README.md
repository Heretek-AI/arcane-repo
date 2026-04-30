# Joern — Code Analysis Platform

[Joern](https://joern.io) is an open-source code analysis platform. It parses source code into code property graphs (CPGs) and provides a query interface for discovering vulnerabilities, tracking data flow, mapping control flow, and auditing dependencies across C/C++, Java, JavaScript/TypeScript, Python, Go, and more.

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

## Using the CLI

To use Joern in CLI mode, set `JOERN_SERVER=false` and run:

```bash
docker compose up -d
docker compose exec joern joern
```

Then execute queries interactively:

```
joern> importCpg("path/to/cpg.bin")
joern> cpg.method.name("exec").callIn.l
```

## Importing Source Code

Mount your source code into the container. Uncomment the volume in `docker-compose.yml`:

```yaml
volumes:
  - ./source-code:/app/source-code:ro
```

Then create a CPG:

```bash
curl -X POST http://localhost:8080/import \
  -H "Content-Type: application/json" \
  -d '{"path": "/app/source-code"}'
```

## Health Check

```bash
curl http://localhost:8080/health
```

A healthy server responds with:
```json
{"status": "ok", "version": "2.x.x"}
```

## Managing Joern

**View logs:**

```bash
docker compose logs -f joern
```

**Increase JVM heap for large codebases:**

Edit your `.env` file:

```
JOERN_OPTS=-Xmx8G
```

**Restart to apply JVM changes:**

```bash
docker compose down
docker compose up -d
```

## Troubleshooting

| Symptom                                    | Likely Cause         | Fix                                          |
|--------------------------------------------|----------------------|----------------------------------------------|
| Server starts but queries timeout          | JVM heap too small   | Increase `JOERN_OPTS` to `-Xmx8G` or higher   |
| `OutOfMemoryError`                         | Codebase too large   | Reduce the imported codebase or increase heap |
| `Connection refused` on port 8080          | Server still starting| Joern's JVM startup takes 10-30s — check logs |
| Query returns no results                   | CPG not imported     | Import source code first via `/import`        |
