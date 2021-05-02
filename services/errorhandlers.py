import functools


def errorlogger(func, log_level="error"):
    @functools.wraps(func)
    def wrapper_errorlogger(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # TODO: Log error here!
            raise e
    return wrapper_errorlogger


class InvalidDateRangeError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass
