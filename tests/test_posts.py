import pytest
from schemas.schemas import POST_SCHEMA
from utils.helpers import validate_schema


class TestGetPosts:
    """Tests for GET /posts"""

    def test_get_all_posts_status_200(self, api):
        response = api.get("/posts")
        assert response.status_code == 200

    def test_get_all_posts_returns_list(self, api):
        response = api.get("/posts")
        data = response.json()
        assert isinstance(data, list)

    def test_get_all_posts_count(self, api):
        response = api.get("/posts")
        # JSONPlaceholder always has 100 posts
        assert len(response.json()) == 100

    def test_get_single_post_status_200(self, api):
        response = api.get("/posts/1")
        assert response.status_code == 200

    def test_get_single_post_schema(self, api):
        response = api.get("/posts/1")
        validate_schema(response.json(), POST_SCHEMA)

    def test_get_single_post_correct_id(self, api):
        response = api.get("/posts/5")
        assert response.json()["id"] == 5

    def test_get_nonexistent_post_returns_404(self, api):
        response = api.get("/posts/99999")
        assert response.status_code == 404

    @pytest.mark.parametrize("post_id", [1, 10, 50, 100])
    def test_get_post_by_various_ids(self, api, post_id):
        """Parametrized: runs 4 separate tests, one per post_id."""
        response = api.get(f"/posts/{post_id}")
        assert response.status_code == 200
        assert response.json()["id"] == post_id

    def test_filter_posts_by_user(self, api):
        response = api.get("/posts", params={"userId": 1})
        posts = response.json()
        assert len(posts) > 0
        assert all(p["userId"] == 1 for p in posts), "All posts should belong to userId=1"

    def test_response_time_is_acceptable(self, api):
        response = api.get("/posts")
        assert response.elapsed.total_seconds() < 3.0, "Response took too long"

    def test_content_type_is_json(self, api):
        response = api.get("/posts/1")
        assert "application/json" in response.headers["Content-Type"]


class TestCreatePost:
    """Tests for POST /posts"""

    def test_create_post_status_201(self, api, new_post_payload):
        response = api.post("/posts", payload=new_post_payload)
        assert response.status_code == 201

    def test_create_post_returns_id(self, api, new_post_payload):
        response = api.post("/posts", payload=new_post_payload)
        assert "id" in response.json()

    def test_create_post_body_matches_payload(self, api, new_post_payload):
        response = api.post("/posts", payload=new_post_payload)
        data = response.json()
        assert data["title"] == new_post_payload["title"]
        assert data["body"] == new_post_payload["body"]
        assert data["userId"] == new_post_payload["userId"]

    def test_create_post_schema(self, api, new_post_payload):
        response = api.post("/posts", payload=new_post_payload)
        validate_schema(response.json(), POST_SCHEMA)


class TestUpdatePost:
    """Tests for PUT and PATCH /posts/{id}"""

    def test_put_post_status_200(self, api):
        payload = {"id": 1, "title": "Updated Title", "body": "Updated body", "userId": 1}
        response = api.put("/posts/1", payload=payload)
        assert response.status_code == 200

    def test_put_post_title_updated(self, api):
        payload = {"id": 1, "title": "Brand New Title", "body": "body", "userId": 1}
        response = api.put("/posts/1", payload=payload)
        assert response.json()["title"] == "Brand New Title"

    def test_patch_post_status_200(self, api):
        response = api.patch("/posts/1", payload={"title": "Patched Title"})
        assert response.status_code == 200

    def test_patch_post_only_updates_field(self, api):
        response = api.patch("/posts/1", payload={"title": "Patched Only"})
        data = response.json()
        assert data["title"] == "Patched Only"
        # Other fields should still exist
        assert "body" in data
        assert "userId" in data


class TestDeletePost:
    """Tests for DELETE /posts/{id}"""

    def test_delete_post_status_200(self, api):
        response = api.delete("/posts/1")
        assert response.status_code == 200

    def test_delete_post_returns_empty_body(self, api):
        response = api.delete("/posts/1")
        # JSONPlaceholder returns {} on delete
        assert response.json() == {}
