from flask import Blueprint
from flask import url_for, request, abort

from resources.errorhandlers import apierrorhandler
from resources.util import build_response
from services.class_service import get_classes, get_class
from services.sample_service import get_samples
from util.customerrors import DatabaseConnectionError

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
@apierrorhandler
def fetch_samples():
    sample_classes = request.args.get("sample_classes")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    quant_method = request.args.get("quant_method")

    sample_list = get_samples(sample_classes, start_time, end_time, quant_method)
    return build_response(
        200,
        samples=sample_list
    )


@api.route("/samples/classes", methods=["GET"])
def fetch_classes():
    classes = get_classes()
    return build_response(
        200,
        classes=classes
    )


@api.route("/samples/classes/<int:class_id>", methods=["GET"])
def fetch_class(class_id):
    class_fetched = get_class(class_id)
    return build_response(
        200,
        **{"class": class_fetched}
    )


@api.route("/<path:text>")
def not_found(text):
    abort(404, "Resource '%s' not found." % text)
