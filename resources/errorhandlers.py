from resources.util import build_response


def not_found_handler(error):
    return build_response(
        404,
        msg=error.description if len(error.description) > 0 else "Resource not found."
    ), 404
