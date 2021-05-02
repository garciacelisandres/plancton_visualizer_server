from pymongo.errors import ConnectionFailure


def errorlogger(func, log_level="error"):
    try:
        func()
    except Exception as e:
        # TODO: Log error here!
        raise e


def connectionlosthandler(func):
    try:
        func()
    except ConnectionFailure as cf:
        # TODO: Log error here!
        pass
