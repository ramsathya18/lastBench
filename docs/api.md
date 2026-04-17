# API Reference (MVP)

Base URL: `/api/v1`

## Auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`

### Example: register
```json
POST /auth/register
{
  "email": "learner@demo.local",
  "password": "password123",
  "full_name": "Demo Learner"
}
```

### Example: login response
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

## Courses and learning
- `GET /courses` (public published catalog, admin sees all when authenticated)
- `GET /courses/{slug}`
- `POST /courses/{course_id}/enroll`
- `GET /me/enrollments`
- `POST /lessons/{lesson_id}/start`
- `POST /lessons/{lesson_id}/complete`
- `GET /me/courses/{course_id}/progress`

### Example: enrollments response
```json
[
  {
    "id": 1,
    "course_id": 5,
    "course_slug": "prompt-engineering-foundations",
    "course_title": "Prompt Engineering Foundations",
    "enrolled_at": "2026-04-17T12:00:00",
    "status": "active"
  }
]
```

## Quiz
- `GET /lessons/{lesson_id}/quiz`
- `POST /quizzes/{quiz_id}/submit`
- `GET /me/quizzes/{quiz_id}/attempts`

### Example: submit quiz
```json
POST /quizzes/12/submit
{
  "answers": [
    { "question_id": 71, "selected_indexes": [1] }
  ]
}
```

## Sandbox (Prompt Sandbox MVP)
- `GET /lessons/{lesson_id}/sandbox`
- `POST /sandbox/tasks/{task_id}/run`
- `GET /me/sandbox/runs`

### Example: run sandbox task
```json
POST /sandbox/tasks/4/run
{ "submitted_content": "My answer with success criteria" }
```

## Admin
- `POST /admin/courses`
- `PATCH /admin/courses/{id}`
- `DELETE /admin/courses/{id}`
- `POST /admin/courses/{course_id}/modules`
- `PATCH /admin/modules/{id}`
- `POST /admin/modules/{module_id}/lessons`
- `PATCH /admin/lessons/{id}`
- `DELETE /admin/lessons/{id}`
- `POST /admin/lessons/{lesson_id}/quiz`
- `POST /admin/lessons/{lesson_id}/sandbox`
- `GET /admin/analytics/overview`

## Auth notes
- Protected endpoints require `Authorization: Bearer <access_token>`.
- Refresh endpoint expects a refresh token body payload and returns a new token pair.

## Error convention
API returns:
```json
{ "error": { "message": "..." } }
```

Common status codes:
- `400` validation/business errors (e.g., duplicate slug)
- `401` auth required / invalid token
- `403` RBAC denial
- `404` not found
- `500` unexpected server error
