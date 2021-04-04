from flask import Blueprint

from resources.util import build_response


api_errors = Blueprint("api_errors", __name__)


@api_errors.errorhandler(400)
def bad_request_handler(error):
    return build_response(
        400,
        code=error.description if len(error.description) > 0 else "Bad request."
    ), 400


def not_found_handler(error):
    return build_response(
        404,
        msg=error.description if len(error.description) > 0 else "Resource not found."
    ), 404


@api_errors.errorhandler(500)
def internal_error_handler(error):
    return build_response(
        500,
        code=error.description if len(error.description) > 0 else "Internal server error."
    ), 500
