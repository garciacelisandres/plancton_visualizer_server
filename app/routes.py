from flask import url_for, request, abort

from app import app
from app.util import get_db, build_response

from datetime import datetime


@app.route("/api/v0.1", methods=["GET"])
def fetch_api_endpoints():
    return build_response(200, links=[
        url_for("fetch_api_endpoints"),
        url_for("fetch_samples"),
        url_for("fetch_classes"),
        url_for("fetch_class", class_id="1")
    ])


@app.route("/api/v0.1/samples", methods=["GET"])
def fetch_samples():
    request_body = request.get_json(force=True)
    if not request_body:
        abort(400, "Bad request.")
    try:
        sample_classes = request_body["sample_classes"]
    except KeyError:
        sample_classes = None
    start_time = datetime.utcfromtimestamp(request_body["start_time"])
    end_time = datetime.utcfromtimestamp(request_body["end_time"])
    try:
        sample_list = get_db(app).get_samples(sample_classes, start_time, end_time)
        return build_response(
            200,
            samples=sample_list
        )
    except ValueError:
        abort(400, "Bad request. \"start_time\" cannot be greater than \"end_time\".")
    except InterruptedError:
        abort(500)


@app.route("/api/v0.1/samples/classes", methods=["GET"])
def fetch_classes():
    try:
        classes = get_db(app).get_classes()
        return build_response(
            200,
            classes=classes
        )
    except InterruptedError:
        abort(500)


@app.route("/api/v0.1/samples/classes/<int:class_id>", methods=["GET"])
def fetch_class(class_id):
    try:
        class_fetched = get_db(app).get_class(class_id)
        return build_response(
            200,
            **{"class": class_fetched}
        )
    except InterruptedError:
        abort(500)


@app.route("/api/v0.1/<path:text>")
def not_found(text):
    abort(404, "Resource \"%s\" not found." % text)
