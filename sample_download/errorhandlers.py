import functools

from database import get_db


def checkdatabaseavailable(func, log_level="error"):
    @functools.wraps(func)
    def wrapper_checkdatabaseavailable(*args, **kwargs):
        db = get_db()
        if not db:
            # TODO: Log error here!
            print(f"A connection could not be made with the database. "
                  f"Skipping execution of {func.__name__!r} function.")
            return
        return func(*args, **kwargs)
    return wrapper_checkdatabaseavailable
