import datetime

from flask import jsonify

from json import JSONEncoder
from bson import ObjectId


def build_response(status, **kwargs):
    response_dict = {"status": status}
    for key, value in kwargs.items():
        response_dict[key] = value
    return jsonify(response_dict)


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o.timestamp())

        return super().default(o)
