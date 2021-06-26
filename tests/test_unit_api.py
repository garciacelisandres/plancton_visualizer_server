import json

import pytest
from pytest_mock import MockerFixture

from resources.create import create_app
from util.customerrors import InvalidDateRangeError, DatabaseConnectionError

mock_sample_list = [
    {"_id": 1, "name": "sample1"},
    {"_id": 2, "name": "sample2"},
    {"_id": 3, "name": "sample3"}
]

processed_sample_list = [
    {"id": 1, "name": "sample1"},
    {"id": 2, "name": "sample2"},
    {"id": 3, "name": "sample3"}
]

class_list = [
    {"_id": 1, "name": "class1"},
    {"_id": 2, "name": "class1"},
    {"_id": 3, "name": "class1"}
]

class_list_processed = [
    {"id": 1, "name": "class1"},
    {"id": 2, "name": "class1"},
    {"id": 3, "name": "class1"}
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
    mocker.patch("resources.routes.get_samples", return_value=[])
    res = client.get("/api/v0.1/samples")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == []


def test_api_fetch_samples_params(client, mocker: MockerFixture):
    mock_sample_list_copy = [
        {"_id": 1, "name": "sample1"},
        {"_id": 2, "name": "sample2"},
        {"_id": 3, "name": "sample3"}
    ]
    patcher = mocker.patch(
        "resources.routes.get_samples",
        return_value=mock_sample_list_copy
    )
    # Test with no parameters
    res = client.get("/api/v0.1/samples")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == processed_sample_list
    patcher.assert_called_once_with(None, None, None, None)

    mock_sample_list_copy = [
        {"_id": 1, "name": "sample1"},
        {"_id": 2, "name": "sample2"},
        {"_id": 3, "name": "sample3"}
    ]
    patcher = mocker.patch(
        "resources.routes.get_samples",
        return_value=mock_sample_list_copy
    )
    # Test with "sample_classes" param
    res = client.get("/api/v0.1/samples?sample_classes=1,2")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == processed_sample_list
    patcher.assert_called_with("1,2", None, None, None)

    mock_sample_list_copy = [
        {"_id": 1, "name": "sample1"},
        {"_id": 2, "name": "sample2"},
        {"_id": 3, "name": "sample3"}
    ]
    patcher = mocker.patch(
        "resources.routes.get_samples",
        return_value=mock_sample_list_copy
    )
    # Test with "start_time" param
    res = client.get("/api/v0.1/samples?start_time=1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == processed_sample_list
    patcher.assert_called_with(None, "1", None, None)

    mock_sample_list_copy = [
        {"_id": 1, "name": "sample1"},
        {"_id": 2, "name": "sample2"},
        {"_id": 3, "name": "sample3"}
    ]
    patcher = mocker.patch(
        "resources.routes.get_samples",
        return_value=mock_sample_list_copy
    )
    # Test with "end_time" param
    res = client.get("/api/v0.1/samples?end_time=1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == processed_sample_list
    patcher.assert_called_with(None, None, "1", None)

    mock_sample_list_copy = [
        {"_id": 1, "name": "sample1"},
        {"_id": 2, "name": "sample2"},
        {"_id": 3, "name": "sample3"}
    ]
    patcher = mocker.patch(
        "resources.routes.get_samples",
        return_value=mock_sample_list_copy
    )
    # Test with "quant_method" param
    res = client.get("/api/v0.1/samples?quant_method=1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["samples"] == processed_sample_list
    patcher.assert_called_with(None, None, None, "1")


def test_api_fetch_samples_params_errors(client, mocker: MockerFixture):
    patcher = mocker.patch(
        "resources.routes.get_samples",
        side_effect=InvalidDateRangeError
    )
    # Test with "start_time" param greater than "end_time" param
    res = client.get("/api/v0.1/samples?start_time=2&end_time=1")
    res = json.loads(res.data)
    assert res["status"] == 400
    assert res["code"] == "Bad request. \"start_time\" cannot be greater than \"end_time\"."
    patcher.assert_called_with(None, "2", "1", None)

    patcher = mocker.patch(
        "resources.routes.get_samples",
        side_effect=DatabaseConnectionError
    )
    # Test with database connection error
    res = client.get("/api/v0.1/samples")
    res = json.loads(res.data)
    assert res["status"] == 500
    assert res["code"] == "A connection error occurred. If this keeps happening, " \
                          "contact the administrator of the system."
    patcher.assert_called_with(None, None, None, None)

    patcher = mocker.patch(
        "resources.routes.get_samples",
        side_effect=Exception
    )
    # Test with generic error
    res = client.get("/api/v0.1/samples")
    res = json.loads(res.data)
    assert res["status"] == 500
    assert res["code"] == "An unexpected error occurred. If this keeps happening, " \
                          "contact the administrator of the system."
    patcher.assert_called_with(None, None, None, None)


def test_api_fetch_classes_empty(client, mocker: MockerFixture):
    mocker.patch(
        "resources.routes.get_classes",
        return_value=[]
    )
    res = client.get("/api/v0.1/samples/classes")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["classes"] == []


def test_api_fetch_class_empty(client, mocker: MockerFixture):
    mocker.patch(
        "resources.routes.get_class",
        return_value=None
    )
    res = client.get("/api/v0.1/samples/classes/1")
    assert res.status_code == 200
    fetched = json.loads(res.data)
    assert fetched["class"] is None


def test_api_not_found(client):
    res = client.get("/api/v0.1/nonexistent")
    assert res.status_code == 404
