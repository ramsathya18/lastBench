# Roadmap

## MVP delivered
- Auth with JWT access/refresh and RBAC.
- Course/module/lesson content model and admin APIs.
- Learner enrollment, lesson progression, quiz attempts, sandbox runs.
- Prompt sandbox MVP with persisted run history.
- Dockerized local setup + realistic seed content.

## Hardening pass delivered
- Architecture consistency fixes (public catalog + admin-only draft visibility).
- Better admin UX for managing course lifecycle.
- Cleaner learner flow messaging and navigation controls.
- Progress logic validation tests for article lifecycle.
- Expanded API docs and setup docs.

## Known limitations
- Prompt sandbox is intentionally constrained (no arbitrary code execution).
- Refresh token revocation list not yet implemented.
- Admin panel focuses on course-level workflows; deeper lesson authoring UX can be expanded.

## Next phase
- Add module/lesson visual editors and drag-drop ordering.
- Add learner activity timeline and recent attempts widgets.
- Introduce secure isolated code execution service for Python sandbox.
- Add CI pipeline for lint/test/build across web and API.
