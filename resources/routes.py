from flask import url_for, request, abort
from flask import Blueprint

from resources.util import build_response
from services.sample_service import get_samples
from services.class_service import get_classes, get_class


api = Blueprint("api", __name__)


@api.route("/", methods=["GET"])
def fetch_api_endpoints():
    return build_response(200, links=[
        url_for("api.fetch_api_endpoints"),
        url_for("api.fetch_samples"),
        url_for("api.fetch_classes"),
        url_for("api.fetch_class", class_id="1")
    ])


@api.route("/samples", methods=["GET"])
def fetch_samples():
    sample_classes = request.args.get("sample_classes")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    quant_method = request.args.get("quant_method")
    try:
        sample_list = get_samples(sample_classes, start_time, end_time, quant_method)
        return build_response(
            200,
            samples=sample_list
        )
    except ValueError:
        abort(400, "Bad request. \"start_time\" cannot be greater than \"end_time\".")
    except InterruptedError as e:
        print(e)
        abort(500)


@api.route("/samples/classes", methods=["GET"])
def fetch_classes():
    try:
        classes = get_classes()
        return build_response(
            200,
            classes=classes
        )
    except InterruptedError:
        abort(500)


@api.route("/samples/classes/<int:class_id>", methods=["GET"])
def fetch_class(class_id):
    try:
        class_fetched = get_class(class_id)
        return build_response(
            200,
            **{"class": class_fetched}
        )
    except InterruptedError:
        abort(500)


@api.route("/<path:text>")
def not_found(text):
    abort(404, "Resource '%s' not found." % text)
