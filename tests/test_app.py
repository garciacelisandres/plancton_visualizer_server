import json

import pytest
from pytest_mock import MockerFixture

from resources.create import create_app

sample_list = [
    {"_id": 1, "name": "sample1"},
    {"_id": 2, "name": "sample2"},
    {"_id": 3, "name": "sample3"}
]

class_list = [
    {"_id": 1, "name": "class1"},
    {"_id": 2, "name": "class1"},
    {"_id": 3, "name": "class1"}
]


@pytest.fixture
def client():
    app = create_app("test")
    client = app.test_client()
    return client


def test_api_fetch_endpoints(client):
    res = client.get("/api/v0.1/")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    expected = [
        "/api/v0.1/",
        "/api/v0.1/samples",
        "/api/v0.1/samples/classes",
        "/api/v0.1/samples/classes/1",
    ]
    assert fetched["links"] == expected


def test_api_fetch_samples_empty(client, mocker: MockerFixture):
    mocker.patch("services.sample_service.get_samples", return_value=[])
    res = client.get("/api/v0.1/samples")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == []


def test_api_fetch_samples_params(client, mocker: MockerFixture):
    patcher = mocker.patch(
        "resources.routes.get_samples",
        return_value=sample_list
    )

    # Test with no parameters
    res = client.get("/api/v0.1/samples")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == sample_list
    patcher.assert_called_once_with(None, None, None, None)

    # Test with "sample_classes" param
    res = client.get("/api/v0.1/samples?sample_classes=1,2")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == sample_list
    patcher.assert_called_with("1,2", None, None, None)

    # Test with "start_time" param
    res = client.get("/api/v0.1/samples?start_time=1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == sample_list
    patcher.assert_called_with(None, "1", None, None)

    # Test with "end_time" param
    res = client.get("/api/v0.1/samples?end_time=1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == sample_list
    patcher.assert_called_with(None, None, "1", None)

    # Test with "quant_method" param
    res = client.get("/api/v0.1/samples?quant_method=1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == sample_list
    patcher.assert_called_with(None, None, None, "1")


def test_api_fetch_classes_empty(client):
    res = client.get("/api/v0.1/samples/classes")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["classes"] == []


def test_api_fetch_class_empty(client):
    res = client.get("/api/v0.1/samples/classes/1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["class"] is None


def test_api_not_found(client):
    res = client.get("/api/v0.1/nonexistent")
    assert res.status_code == 404
