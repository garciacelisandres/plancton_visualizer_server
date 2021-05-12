from services.errorhandlers import errorlogger
from services.util import get_db_check_initialized


@errorlogger
def get_classes():
    class_list = get_db_check_initialized().get_classes()
    return class_list


@errorlogger
def get_class(class_id: int):
    found_class = get_db_check_initialized().get_class(class_id)
    return found_class
