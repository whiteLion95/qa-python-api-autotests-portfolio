import pytest
from schemas.schemas import COMMENT_SCHEMA
from utils.helpers import validate_schema, is_valid_email


class TestGetComments:

    def test_get_all_comments_status_200(self, api):
        response = api.get("/comments")
        assert response.status_code == 200

    def test_get_all_comments_count(self, api):
        response = api.get("/comments")
        assert len(response.json()) == 500

    def test_get_comment_by_id_schema(self, api):
        response = api.get("/comments/1")
        validate_schema(response.json(), COMMENT_SCHEMA)

    def test_filter_comments_by_post_id(self, api):
        response = api.get("/comments", params={"postId": 1})
        comments = response.json()
        assert len(comments) > 0
        assert all(c["postId"] == 1 for c in comments)

    def test_all_comment_emails_are_valid(self, api):
        """Every comment has an email field — all should be valid format."""
        comments = api.get("/comments", params={"postId": 1}).json()
        for comment in comments:
            assert is_valid_email(comment["email"]), \
                f"Invalid email in comment id={comment['id']}: {comment['email']}"

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_each_post_has_5_comments(self, api, post_id):
        """JSONPlaceholder gives exactly 5 comments per post."""
        response = api.get("/comments", params={"postId": post_id})
        assert len(response.json()) == 5

    def test_comment_body_is_not_empty(self, api):
        response = api.get("/comments/1")
        assert response.json()["body"].strip() != ""

    def test_get_nonexistent_comment_404(self, api):
        response = api.get("/comments/99999")
        assert response.status_code == 404
