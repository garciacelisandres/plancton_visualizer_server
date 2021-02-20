from app import app

from app.util import build_response


@app.errorhandler(400)
def not_found_handler(error):
    return build_response(
        400,
        code=error.description if len(error.description) > 0 else "Bad request."
    ), 400


@app.errorhandler(404)
def not_found_handler(error):
    return build_response(
        404,
        code=error.description if len(error.description) > 0 else "Resource not found."
    ), 404


@app.errorhandler(500)
def not_found_handler(error):
    return build_response(
        500,
        code=error.description if len(error.description) > 0 else "Internal server error."
    ), 500
