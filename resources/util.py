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


def convert_ids_obj(data: dict or None, url: str = None) -> dict or None:
    if not data:
        return data
    copy = data.copy()
    obj_id = copy.pop("_id")
    copy["id"] = obj_id
    if url and len(url.strip()) > 0:
        copy["links"] = {"self": f"{url}/{obj_id}"}
    return copy


def convert_ids_list(data: list, url: str = None) -> list:
    copy = data.copy()
    for obj in copy:
        obj_id = obj.pop("_id")
        obj["id"] = obj_id
        if url and len(url.strip()) > 0:
            obj["links"] = {"self": f"{url}/{obj_id}"}
    return copy
