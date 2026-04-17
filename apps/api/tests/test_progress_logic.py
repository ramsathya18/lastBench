
def bootstrap_article_lesson(client, admin_headers):
    course = client.post(
        "/api/v1/admin/courses",
        headers=admin_headers,
        json={
            "title": "Progress Course",
            "slug": "progress-course",
            "description": "",
            "difficulty": "beginner",
            "estimated_minutes": 30,
            "tags": [],
            "thumbnail_url": "",
            "status": "published",
        },
    ).json()
    module = client.post(
        f"/api/v1/admin/courses/{course['id']}/modules",
        headers=admin_headers,
        json={"title": "M1", "description": "", "sort_order": 1},
    ).json()
    lesson = client.post(
        f"/api/v1/admin/modules/{module['id']}/lessons",
        headers=admin_headers,
        json={
            "title": "Intro",
            "slug": "progress-intro",
            "summary": "",
            "lesson_type": "article",
            "content_markdown": "Hi",
            "estimated_minutes": 5,
            "sort_order": 1,
            "status": "published",
        },
    ).json()
    return course, lesson


def test_article_progress_requires_complete_action(client):
    client.post("/api/v1/auth/register", json={"email": "admin2@admin.local", "password": "secret123", "full_name": "Admin"})
    admin_token = client.post("/api/v1/auth/login", json={"email": "admin2@admin.local", "password": "secret123"}).json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    course, lesson = bootstrap_article_lesson(client, admin_headers)

    client.post("/api/v1/auth/register", json={"email": "learner2@test.com", "password": "secret123", "full_name": "Learner"})
    token = client.post("/api/v1/auth/login", json={"email": "learner2@test.com", "password": "secret123"}).json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}

    client.post(f"/api/v1/courses/{course['id']}/enroll", headers=h)
    start = client.post(f"/api/v1/lessons/{lesson['id']}/start", headers=h).json()
    assert start["status"] == "in_progress"

    before = client.get(f"/api/v1/me/courses/{course['id']}/progress", headers=h).json()
    assert before["completion_percent"] == 0

    done = client.post(f"/api/v1/lessons/{lesson['id']}/complete", headers=h).json()
    assert done["status"] == "completed"

    after = client.get(f"/api/v1/me/courses/{course['id']}/progress", headers=h).json()
    assert after["completion_percent"] == 100.0
