from pymongo.errors import ConnectionFailure
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


def connectionlosthandler(func):
    @functools.wraps(func)
    def wrapper_connectionlosthandler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionFailure:
            # TODO: Log error here!
            pass
    return wrapper_connectionlosthandler
