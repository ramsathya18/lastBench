
def bootstrap_course(client, admin_headers):
    c = client.post("/api/v1/admin/courses", headers=admin_headers, json={
        "title": "Course 1",
        "slug": "course-1",
        "description": "desc",
        "difficulty": "beginner",
        "estimated_minutes": 60,
        "tags": ["ai"],
        "thumbnail_url": "",
        "status": "published",
    }).json()
    m = client.post(f"/api/v1/admin/courses/{c['id']}/modules", headers=admin_headers, json={"title":"M1","description":"","sort_order":1}).json()
    l = client.post(f"/api/v1/admin/modules/{m['id']}/lessons", headers=admin_headers, json={
        "title":"L1","slug":"l1","summary":"","lesson_type":"quiz","content_markdown":"","estimated_minutes":5,"sort_order":1,"status":"published"
    }).json()
    return c, m, l


def test_auth_course_enrollment_quiz_progress_sandbox(client):
    client.post("/api/v1/auth/register", json={"email": "boss@admin.local", "password": "secret123", "full_name": "Boss"})
    admin_token = client.post("/api/v1/auth/login", json={"email": "boss@admin.local", "password": "secret123"}).json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    c, _m, l = bootstrap_course(client, admin_headers)

    client.post("/api/v1/admin/lessons/{}/quiz".format(l["id"]), headers=admin_headers, json={
        "title": "Quiz 1",
        "passing_score": 50,
        "questions": [{"question_text":"2+2?","options_json":["3","4"],"correct_answer_json":[1],"explanation":"basic"}]
    })
    client.post("/api/v1/admin/lessons/{}/sandbox".format(l["id"]), headers=admin_headers, json={
        "title":"Prompt Task",
        "instructions":"Include MVP",
        "starter_template":"Answer...",
        "validator_config":{"must_include":"MVP"}
    })

    client.post("/api/v1/auth/register", json={"email": "learner@test.com", "password": "secret123", "full_name": "Learner"})
    token = client.post("/api/v1/auth/login", json={"email": "learner@test.com", "password": "secret123"}).json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}

    assert client.get("/api/v1/courses", headers=h).status_code == 200
    assert client.post(f"/api/v1/courses/{c['id']}/enroll", headers=h).status_code == 200
    assert client.post(f"/api/v1/lessons/{l['id']}/start", headers=h).status_code == 200

    quiz = client.get(f"/api/v1/lessons/{l['id']}/quiz", headers=h).json()
    submit = client.post(f"/api/v1/quizzes/{quiz['id']}/submit", headers=h, json={"answers":[{"question_id":quiz['questions'][0]['id'],"selected_indexes":[1]}]}).json()
    assert submit["passed"] is True

    progress = client.get(f"/api/v1/me/courses/{c['id']}/progress", headers=h).json()
    assert progress["completed_lessons"] >= 1

    task = client.get(f"/api/v1/lessons/{l['id']}/sandbox", headers=h).json()
    run = client.post(f"/api/v1/sandbox/tasks/{task['id']}/run", headers=h, json={"submitted_content":"This is MVP answer"}).json()
    assert run["score_or_result"]["passed"] is True
