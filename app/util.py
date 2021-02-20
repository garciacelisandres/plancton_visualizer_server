from flask import Flask, jsonify

from database.database_api import Database


def get_db(app: Flask) -> Database:
    return app.config["DB_CONNECTION"]


def build_response(status, **kwargs):
    response_dict = {"status": status}
    for key, value in kwargs.items():
        response_dict[key] = value
    return jsonify(response_dict)
