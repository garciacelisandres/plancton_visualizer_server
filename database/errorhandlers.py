import functools
import logging

from pymongo.errors import ConnectionFailure

from util.customerrors import DatabaseConnectionError


def errorlogger(func):
    @functools.wraps(func)
    def wrapper_errorlogger(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionFailure as cf:
            raise cf
        except Exception as e:
            logging.error("The following error occurred in the database: %s" % e)
            raise e

    return wrapper_errorlogger


def connectionlosthandler(func):
    @functools.wraps(func)
    def wrapper_connectionlosthandler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionFailure as e:
            logging.error("Connection with the database is nonexistent. Error details: %s" % e)
            raise DatabaseConnectionError

    return wrapper_connectionlosthandler
