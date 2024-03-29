from flask import Blueprint
from flask import url_for, request, abort

from resources.util import build_response, convert_ids_obj, convert_ids_list
from services.class_service import get_classes, get_class
from services.sample_service import get_samples
from util.customerrors import InvalidDateRangeError, DatabaseConnectionError, ClassNotFoundError

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

    sample_list = convert_ids_list(get_samples(sample_classes, start_time, end_time, quant_method))
    return build_response(
        200,
        samples=sample_list
    )


@api.route("/samples/classes", methods=["GET"])
def fetch_classes():
    classes = convert_ids_list(get_classes(), url_for("api.fetch_classes"))
    return build_response(
        200,
        classes=classes
    )


@api.route("/samples/classes/<string:class_id>", methods=["GET"])
def fetch_class(class_id):
    class_fetched = get_class(class_id)
    processed = convert_ids_obj(class_fetched, url_for("api.fetch_class", class_id=class_id))
    return build_response(
        200,
        **{"class": processed}
    )


@api.route("/<path:text>")
def not_found(text):
    abort(404, "Resource '%s' not found." % text)


@api.errorhandler(InvalidDateRangeError)
def invalid_date_range_error_handler(error):
    return build_response(
        400,
        code='Bad request. "start_time" cannot be greater than "end_time".'
    ), 400


@api.errorhandler(ClassNotFoundError)
def class_not_found_error_handler(error):
    return build_response(
        404,
        code=f"Resource not found. The class with ID {error.class_id} was not found."
    ), 404


@api.errorhandler(DatabaseConnectionError)
def database_connection_error_handler(error):
    return build_response(
        500,
        code="A connection error occurred. If this keeps happening, contact the administrator of the system."
    ), 500


@api.errorhandler(Exception)
def generic_error_handler(error):
    return build_response(
        500,
        code="An unexpected error occurred. If this keeps happening, contact the administrator of the system."
    ), 500
