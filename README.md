# Learning Platform MVP

Production-style MVP for hosting structured learning content with progress tracking, quizzes, sandbox exercises, learner dashboards, and admin content operations.

## Stack
- **Frontend:** Next.js 15 + TypeScript + App Router + Tailwind CSS
- **UI:** Tailwind + reusable component primitives (shadcn-aligned patterns)
- **Backend:** FastAPI + Python 3.12 + SQLAlchemy 2.x + Alembic
- **Database:** PostgreSQL
- **Auth:** JWT access/refresh with RBAC (admin + learner)
- **Infra:** Docker Compose

## Repo layout
```text
apps/
  api/  # FastAPI backend
  web/  # Next.js frontend
docs/   # architecture, api, setup, roadmap
scripts/# seed + dev helpers
```

## Quick start
1. Copy env template:
   ```bash
   cp .env.example .env
   ```
2. Start local stack:
   ```bash
   docker compose up --build
   ```
3. Run seed data (from repo root):
   ```bash
   docker compose exec api python /scripts/seed_demo_data.py
   ```
4. Open:
   - Web: http://localhost:3000
   - API docs: http://localhost:8000/docs

## Demo accounts
- **Admin:** `admin@demo.local` / `password123`
- **Learner:** `learner@demo.local` / `password123`

## What improved in hardening pass
- Cleaner API auth/public boundaries and stronger admin CRUD validation.
- Better learner flow feedback (no blocking browser alerts, clearer states).
- Improved admin UX: table-based course management + edit/create feedback.
- Progress logic hardened and expanded tests for article progress flow.
- More realistic seed data with curated modules/lesson narratives.
- Docker setup tightened with DB healthcheck + `.env` usage.
- API docs expanded with error format and examples.

## Screenshots (placeholders)
> Add real images after running locally. Suggested filenames shown below.

1. `docs/screenshots/01-home.png` — Home page hero and nav
2. `docs/screenshots/02-catalog.png` — Course catalog cards
3. `docs/screenshots/03-course-detail.png` — Course detail with modules and enroll CTA
4. `docs/screenshots/04-learn-article.png` — Learning view (article + sidebar)
5. `docs/screenshots/05-learn-quiz.png` — Quiz interaction flow
6. `docs/screenshots/06-learn-sandbox.png` — Prompt sandbox run panel
7. `docs/screenshots/07-dashboard.png` — Learner dashboard progress cards
8. `docs/screenshots/08-admin-courses.png` — Admin course management table
9. `docs/screenshots/09-admin-edit-course.png` — Admin edit course form
10. `docs/screenshots/10-admin-analytics.png` — Admin analytics overview
