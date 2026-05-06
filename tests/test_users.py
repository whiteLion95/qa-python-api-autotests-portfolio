
import pytest
from schemas.schemas import USER_SCHEMA
from utils.helpers import validate_schema, is_valid_email


class TestGetUsers:

    def test_get_all_users_status_200(self, api):
        response = api.get("/users")
        assert response.status_code == 200

    def test_get_all_users_returns_10_records(self, api):
        response = api.get("/users")
        assert len(response.json()) == 10

    def test_get_single_user_schema(self, api):
        response = api.get("/users/1")
        validate_schema(response.json(), USER_SCHEMA)

    def test_user_has_valid_email(self, api):
        response = api.get("/users/1")
        email = response.json()["email"]
        assert is_valid_email(email), f"Email '{email}' is not valid"

    def test_user_has_nested_address(self, api):
        response = api.get("/users/1")
        user = response.json()
        assert "address" in user
        assert "city" in user["address"]
        assert "geo" in user["address"]

    @pytest.mark.parametrize("user_id", [1, 2, 3, 5, 10])
    def test_each_user_has_username(self, api, user_id):
        response = api.get(f"/users/{user_id}")
        assert response.json()["username"] != ""

    def test_all_user_emails_are_valid(self, api):
        users = api.get("/users").json()
        invalid = [u["email"] for u in users if not is_valid_email(u["email"])]
        assert not invalid, f"Invalid emails found: {invalid}"

    def test_get_nonexistent_user_returns_404(self, api):
        response = api.get("/users/9999")
        assert response.status_code == 404


class TestCreateUser:

    def test_create_user_status_201(self, api, new_user_payload):
        response = api.post("/users", payload=new_user_payload)
        assert response.status_code == 201

    def test_create_user_name_matches(self, api, new_user_payload):
        response = api.post("/users", payload=new_user_payload)
        assert response.json()["name"] == new_user_payload["name"]