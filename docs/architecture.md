# Architecture

## System overview
- **Web**: Next.js App Router frontend with feature-first UI modules.
- **API**: FastAPI REST service with router/service/model separation.
- **DB**: PostgreSQL with SQLAlchemy 2.x models and Alembic migrations.
- **Auth**: JWT access + refresh with explicit role guards.

## High-level design
- Frontend calls `/api/v1/*` over REST.
- Public catalog endpoints expose only published content.
- Authenticated learner/admin flows are guarded server-side.
- Progress, quiz attempts, and sandbox runs are persisted and queryable.

## Backend module responsibilities
- `api/auth.py`: registration, login, refresh, me.
- `api/courses.py`: catalog and course detail retrieval.
- `api/learning.py`: enrollment, lesson start/complete, progress, quiz/sandbox learner actions.
- `api/admin.py`: content CRUD, quiz/sandbox authoring, analytics overview.
- `services/*`: progress logic, quiz scoring, sandbox evaluation.

## Data model summary
Core entities: `User`, `Course`, `Module`, `Lesson`, `Enrollment`, `LessonProgress`, `Quiz` (+questions/attempts), `SandboxTask` (+runs).

## Key flows
1. **Auth flow**: register/login -> access+refresh pair.
2. **Learning flow**: enroll -> open lesson (in_progress) -> complete/submit -> progress update.
3. **Admin flow**: create/edit/publish course graph and inspect overview analytics.

## Sandbox architecture (MVP)
- Prompt sandbox only: submitted text is validated against task config (`must_include`) and persisted.
- No arbitrary code execution claims.
- Clear extension path to isolated runtime worker.

## Hardening improvements in this pass
- Unified API error response envelope.
- Duplicate slug guards for courses and lessons.
- Public catalog behavior corrected for published-only unauthenticated access.
- Analytics completion count now based on actual completed lesson progress records.

## Tradeoffs
- No Redis/background worker in MVP to reduce complexity.
- Admin UI remains intentionally lightweight while core CRUD correctness is prioritized.

## Future evolution
- Isolated Python execution service (resource limits + policy engine).
- Refresh token rotation/revocation persistence.
- Rich markdown rendering and content versioning.
