import functools

from flask import Blueprint
from werkzeug.exceptions import abort

from resources.util import build_response
from util.customerrors import InvalidDateRangeError, DatabaseConnectionError

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


def apierrorhandler(func):
    @functools.wraps(func)
    def wrapper_apierrorhandler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidDateRangeError:
            abort(400, "Bad request. \"start_time\" cannot be greater than \"end_time\".")
        except DatabaseConnectionError:
            abort(500, "A connection error occurred. If this keeps happening, contact the administrator of the system.")
        except Exception:
            abort(500,
                  "An unexpected error occurred. If this keeps happening, contact the administrator of the system.")

    return wrapper_apierrorhandler
