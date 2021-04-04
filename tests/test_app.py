import pytest

from resources.create import create_app


@pytest.fixture(autouse=True)
def client():
    app = create_app("test")
    client = app.test_client()
    return client


def test_api_fetch_endpoints(client):
    res = client.get("/api/v0.1")
    print(res)
