import functools
import logging

from pymongo.errors import ConnectionFailure


def errorlogger(func):
    @functools.wraps(func)
    def wrapper_errorlogger(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error("The following error occurred: %s" % e)
            # raise e

    return wrapper_errorlogger


def connectionlosthandler(func):
    @functools.wraps(func)
    def wrapper_connectionlosthandler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionFailure as e:
            logging.error("Connection with the database is nonexistent. %s" % e)

    return wrapper_connectionlosthandler
