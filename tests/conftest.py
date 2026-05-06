
import pytest
from api.client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api():
    """
    Session-scoped fixture: one APIClient instance for the whole test run.
    'session' scope means it's created once and reused — efficient for API tests.
    """
    return APIClient(base_url=BASE_URL)


@pytest.fixture
def new_post_payload():
    """Returns a sample payload for creating a post."""
    return {
        "title": "Automated Test Post",
        "body": "This post was created by a pytest fixture",
        "userId": 1
    }


@pytest.fixture
def new_user_payload():
    """Returns a sample payload for creating a user."""
    return {
        "name": "Jane QA Engineer",
        "username": "jane_qa",
        "email": "jane@qa.com",
    }