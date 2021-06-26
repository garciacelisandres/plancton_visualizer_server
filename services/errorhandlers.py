import functools
import logging


def errorlogger(func):
    @functools.wraps(func)
    def wrapper_errorlogger(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error("The following error occurred: %s" % e)
            raise e

    return wrapper_errorlogger
