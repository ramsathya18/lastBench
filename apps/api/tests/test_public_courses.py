
def test_courses_list_is_public_for_published_content(client):
    client.post("/api/v1/auth/register", json={"email": "admin3@admin.local", "password": "secret123", "full_name": "Admin"})
    token = client.post("/api/v1/auth/login", json={"email": "admin3@admin.local", "password": "secret123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/admin/courses",
        headers=headers,
        json={
            "title": "Public Course",
            "slug": "public-course",
            "description": "",
            "difficulty": "beginner",
            "estimated_minutes": 15,
            "tags": [],
            "thumbnail_url": "",
            "status": "published",
        },
    )

    res = client.get("/api/v1/courses")
    assert res.status_code == 200
    assert len(res.json()) >= 1
