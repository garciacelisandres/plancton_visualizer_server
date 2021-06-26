class InvalidDateRangeError(Exception):
    pass


class ClassNotFoundError(Exception):
    def __init__(self, class_id):
        self.class_id = class_id


class DatabaseConnectionError(Exception):
    pass
