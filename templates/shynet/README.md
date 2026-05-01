# Shynet — Privacy-Friendly Web Analytics

> **No Docker image — deploy as a Django application.**
> [Shynet](https://github.com/milesmcc/shynet) is a modern, privacy-friendly,
> cookie-free web analytics platform built with Django. No public Docker image
> or upstream Dockerfile exists — it must be deployed as a Django application
> with PostgreSQL. This Docker template provides a minimal informational
> API stub. Clone the upstream repo and deploy with gunicorn for the full
> analytics platform.

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

Deploy Shynet as a Django application:

```bash
git clone https://github.com/milesmcc/shynet
cd shynet
pip install -r requirements.txt

# Configure PostgreSQL
export DATABASE_URL=postgres://shynet:password@localhost/shynet

python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Production: use gunicorn
gunicorn shynet.wsgi:application -b 0.0.0.0:8000
```

## Configuration

| Variable       | Default  | Description                       |
|----------------|----------|-----------------------------------|
| `SHYNET_PORT`  | `8000`   | Host port for the informational API stub |

## API Endpoints

| Endpoint  | Method | Description                                          |
|-----------|--------|------------------------------------------------------|
| `/health` | GET    | Health check + missing-Dockerfile info               |
| `/guide`  | GET    | Django application deployment instructions             |

## Managing

**View logs:**

```bash
docker compose logs -f shynet
```

## Troubleshooting

| Symptom                          | Likely Cause              | Fix                                                              |
|----------------------------------|---------------------------|------------------------------------------------------------------|
| No analytics functionality       | This is a Docker stub     | Clone and deploy Shynet as a Django app with PostgreSQL          |
| Container exits immediately      | pip install failure       | Run `docker compose logs shynet` for details                     |
| Need analytics dashboard         | Using wrong deployment    | Shynet is a Django project — deploy with gunicorn + PostgreSQL   |
