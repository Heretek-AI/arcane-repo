# Mailcow — Mail Server Suite

> **Circular compose dependency — clone upstream directly.**
> [Mailcow](https://mailcow.email) is a complete mail server suite with Postfix,
> Dovecot, Rspamd, SOGo, and more. The dockerized version
> ([mailcow/mailcow-dockerized](https://github.com/mailcow/mailcow-dockerized))
> IS its own docker-compose repository — wrapping it in another compose would
> be circular. This Docker template provides a minimal informational API stub.
> Clone the upstream repo directly for the full email stack.

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

Deploy Mailcow directly from its compose repository:

```bash
git clone https://github.com/mailcow/mailcow-dockerized
cd mailcow-dockerized
./generate_config.sh
docker compose up -d
```

This gives you the complete stack: Postfix (SMTP), Dovecot (IMAP/POP3), Rspamd (anti-spam), SOGo (webmail/calendar), Redis, MariaDB, ClamAV, and more.

## Why Not a Wrapper?

`mailcow/mailcow-dockerized` is itself a docker-compose project with 20+ services, custom config generation scripts, and integrated orchestration. Wrapping it in another compose file would:
- Break the config generation workflow
- Duplicate 20+ service definitions
- Create version synchronization problems

The right approach is to deploy it directly.

## Configuration

| Variable        | Default  | Description                       |
|-----------------|----------|-----------------------------------|
| `MAILCOW_PORT`  | `8000`   | Host port for the informational API stub |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + circular dependency info              |
| `/guide`  | GET    | Clone-and-deploy instructions for the upstream repo  |

## Managing

**View logs:**

```bash
docker compose logs -f mailcow
```

## Troubleshooting

| Symptom                          | Likely Cause              | Fix                                                              |
|----------------------------------|---------------------------|------------------------------------------------------------------|
| No mail server functionality     | This is a Docker stub     | Clone `mailcow/mailcow-dockerized` and deploy directly           |
| Container exits immediately      | pip install failure       | Run `docker compose logs mailcow` for details                    |
| Need full email stack            | Using wrong deployment    | Mailcow provides its own compose — use it directly               |
