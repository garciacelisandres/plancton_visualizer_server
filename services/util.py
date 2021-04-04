from database.database_api import get_db


def get_db_check_initialized():
    db = get_db()
    if db is None:
        raise ConnectionError("A connection to the database is non-existent; aborting operation.")
    return db
