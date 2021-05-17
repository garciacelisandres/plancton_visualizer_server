import functools
import logging

from database import get_db


def checkdatabaseavailable(func):
    @functools.wraps(func)
    def wrapper_checkdatabaseavailable(*args, **kwargs):
        db = get_db()
        if not db:
            logging.warning(f"A connection could not be made with the database. "
                            f"Skipping execution of {func.__name__!r} function.")
            return False
        return func(*args, **kwargs)

    return wrapper_checkdatabaseavailable
