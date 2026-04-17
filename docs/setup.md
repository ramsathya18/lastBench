# Setup Guide

## Prerequisites
- Docker + Docker Compose v2+

## Environment
1. Copy `.env.example` to `.env`.
2. Set secure values for `API_SECRET_KEY` and `API_REFRESH_SECRET_KEY`.

## Boot local stack
```bash
docker compose up --build
```

Services:
- Web: http://localhost:3000
- API docs: http://localhost:8000/docs
- Postgres: localhost:5432

## Database migrations
- API container runs `alembic upgrade head` on startup.

## Seed demo data
```bash
docker compose exec api python /scripts/seed_demo_data.py
```

## Useful commands
```bash
# rebuild only API
docker compose build api

# run backend tests in container (after adding test deps)
docker compose exec api pytest
```

## Troubleshooting
- If API starts before DB is ready, compose healthchecks now gate startup; restart with `docker compose restart api`.
- If auth fails unexpectedly, ensure web uses `NEXT_PUBLIC_API_BASE_URL` from `.env`.
