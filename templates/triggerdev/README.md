# Trigger.dev — Durable Background Jobs & Workflows

[Trigger.dev](https://trigger.dev) is an open-source platform for creating reliable, long-running background jobs and workflows in TypeScript. It provides durable execution with automatic retries, real-time observability, and first-class support for webhooks, schedules, queues, and delays.

## Quick Start

1. **Generate required secrets and start the server:**

   ```bash
   cp .env.example .env
   # Edit .env — generate each secret with:
   #   openssl rand -hex 32
   docker compose up -d
   ```

2. **Open the dashboard:**

   Navigate to [http://localhost:3030](http://localhost:3030) and sign up (or sign in via GitHub OAuth if configured).

3. **Install the Trigger.dev client SDK in your project:**

   ```bash
   npm install @trigger.dev/sdk@latest
   # or
   yarn add @trigger.dev/sdk@latest
   ```

4. **Create your first job:**

   ```typescript
   import { TriggerClient, eventTrigger } from "@trigger.dev/sdk";

   const client = new TriggerClient({
     id: "my-first-job",
     apiKey: process.env.TRIGGER_SECRET_KEY!,
     apiUrl: "http://localhost:3030",
   });

   client.defineJob({
     id: "hello-world",
     name: "Hello World",
     version: "0.1.0",
     trigger: eventTrigger({
       name: "hello.world",
     }),
     run: async (payload, io) => {
       await io.logger.info("Hello from Trigger.dev!", { payload });
       return { result: "success" };
     },
   });

   client.listen();
   ```

5. **Trigger the job from your application:**

   ```typescript
   await client.sendEvent({
     name: "hello.world",
     payload: { message: "Hello!" },
   });
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

### Mandatory Variables

| Variable              | Description                                                               |
|-----------------------|---------------------------------------------------------------------------|
| `SESSION_SECRET`      | Signs session cookies. Generate: `openssl rand -hex 32`                   |
| `MAGIC_LINK_SECRET`   | Signs magic link tokens. Generate: `openssl rand -hex 32`                 |
| `TRIGGER_SECRET_KEY`  | Authenticates your client SDK. Generate a strong random string.            |
| `ENCRYPTION_KEY`      | Encrypts sensitive data at rest. Generate: `openssl rand -hex 32`         |
| `POSTGRES_PASSWORD`   | Password for the trigger.dev PostgreSQL database                          |

### Optional Variables

| Variable                 | Default          | Description                                         |
|--------------------------|------------------|-----------------------------------------------------|
| `TRIGGERDEV_PORT`        | `3030`           | Host port for the trigger.dev dashboard and API     |
| `APP_ORIGIN`             | `http://localhost:3030` | Public URL of the instance (used for magic links)  |
| `POSTGRES_PORT`          | `5432`           | Host port for PostgreSQL                            |
| `POSTGRES_USER`          | `postgres`       | PostgreSQL user                                     |
| `POSTGRES_DB`            | `triggerdev`     | PostgreSQL database name                            |
| `AUTH_GITHUB_CLIENT_ID`  | (empty)          | GitHub OAuth App client ID                          |
| `AUTH_GITHUB_CLIENT_SECRET` | (empty)       | GitHub OAuth App client secret                      |

## API Endpoints

Trigger.dev exposes the dashboard and API on port 3030:

| Endpoint                        | Description                          |
|---------------------------------|--------------------------------------|
| `/`                             | Dashboard UI                         |
| `/api/v1/`                      | Trigger.dev API (used by the SDK)    |
| `/auth/`                        | Authentication endpoints             |

The SDK connects to the API endpoint at `http://localhost:3030`.

## Health Check

Trigger.dev runs its health checks internally. Verify the service is running:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3030
```

Expected response: `200`

## Creating and Running Jobs

### 1. Initialize your project

```bash
mkdir my-trigger-project && cd my-trigger-project
npm init -y
npm install @trigger.dev/sdk@latest
```

### 2. Create a job file (`jobs/hello.ts`)

```typescript
import { TriggerClient, eventTrigger } from "@trigger.dev/sdk";

const client = new TriggerClient({
  id: "demo-jobs",
  apiKey: process.env.TRIGGER_SECRET_KEY!,
  apiUrl: process.env.TRIGGER_API_URL || "http://localhost:3030",
});

client.defineJob({
  id: "example-job",
  name: "Example Job",
  version: "0.1.0",
  trigger: eventTrigger({ name: "example.event" }),
  run: async (payload, io) => {
    await io.logger.info("Job started", { payload });
    await io.wait("wait-a-bit", 5); // waits 5 seconds
    await io.logger.info("Job finished");
    return { processed: true };
  },
});

client.listen();
```

### 3. Run the job worker

```bash
TRIGGER_SECRET_KEY=your-secret-key TRIGGER_API_URL=http://localhost:3030 npx tsx jobs/hello.ts
```

### 4. Trigger from another process

```typescript
import { TriggerClient } from "@trigger.dev/sdk";

const client = new TriggerClient({
  id: "my-app",
  apiKey: process.env.TRIGGER_SECRET_KEY!,
  apiUrl: "http://localhost:3030",
});

await client.sendEvent({
  name: "example.event",
  payload: { data: "Hello from my app!" },
});
```

## Management

**View logs:**

```bash
docker compose logs -f triggerdev
```

**Reset the database:**

```bash
docker compose down -v
docker compose up -d
```

**Run database migrations (if needed):**

```bash
docker compose exec triggerdev npx prisma migrate deploy
```

## Troubleshooting

| Symptom                                    | Likely Cause                   | Fix                                                         |
|--------------------------------------------|--------------------------------|-------------------------------------------------------------|
| Dashboard returns 500                      | Missing or invalid secrets     | Verify `SESSION_SECRET`, `MAGIC_LINK_SECRET`, `ENCRYPTION_KEY` are set |
| SDK cannot connect (`ECONNREFUSED`)        | Server not ready                | Wait for the server to start (`docker compose logs -f`)     |
| `401 Unauthorized` from SDK                | Wrong `TRIGGER_SECRET_KEY`     | Ensure the value in `.env` matches the one in your SDK config |
| "Invalid `prisma migrate`" errors          | Database not initialized       | The server auto-runs migrations on first start              |
| Magic link emails not sending              | SMTP not configured            | Configure an SMTP provider or email via the trigger.dev dashboard settings |
