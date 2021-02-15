from os import environ

from flask import Flask
from flask import request, jsonify, abort
from flask_cors import CORS

from pymongo import MongoClient
from database import Database

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

db_scheme = environ.get("DATABASE_CONNECTION_SCHEME")
db_netloc = environ.get("DATABASE_CONNECTION_NETLOC")
db_port = environ.get("DATABASE_CONNECTION_PORT")
app.config["DB"] = MongoClient("%s://%s:%s" % (db_scheme, db_netloc, db_port)).plancton


@app.route("/api/v0.1", methods=["GET"])
def fetch_api_endpoints():
    return jsonify({
        "status": 200,
        "links": [
            "/api/v0.1",
            "/api/v0.1/samples",
            "/api/v0.1/samples/classes",
            "/api/v0.1/samples/classes/:class_id:"
        ]
    })


@app.route("/api/v0.1/samples", methods=["GET"])
def fetch_samples():
    request_body = request.get_json(force=True)
    if not request_body:
        return jsonify({
            "status": 400,
            "code": "Bad request. Parameter \"sample_classes\" and at least one of \"start_time\" and \"end_time\" "
                    "required. "
        })
    sample_classes = request_body["sample_classes"]
    start_time = request_body["start_time"]
    end_time = request_body["end_time"]
    try:
        sample_list = Database.get_samples(app.config["DB"], sample_classes, start_time, end_time)
        return jsonify({
            "status": 200,
            "samples": sample_list
        })
    except ValueError:
        return jsonify({
            "status": 400,
            "code": "Bad request. \"start_time\" cannot be greater than \"end_time\"."
        })
    except InterruptedError:
        abort(500)


@app.route("/api/v0.1/samples/classes", methods=["GET"])
def fetch_classes():
    try:
        classes = Database.get_classes(app.config["DB"])
        return jsonify({
            "status": 200,
            "classes": classes
        })
    except InterruptedError:
        abort(500)


@app.route("/api/v0.1/samples/classes/<int:class_id>", methods=["GET"])
def fetch_class(class_id):
    try:
        class_fetched = Database.get_class(app.config["DB"], class_id)
        return jsonify({
            "status": 200,
            "class": class_fetched
        })
    except InterruptedError:
        abort(500)


@app.route("/api/v0.1/<path:text>")
def not_found(text):
    abort(404)


@app.errorhandler(404)
def not_found_handler(err):
    return jsonify({
        "status": 404,
        "code": "Resource not found."
    }), 404


@app.errorhandler(500)
def not_found_handler(err):
    return jsonify({
        "status": 500,
        "code": "Internal server error. Please, try again."
    })


app.run()
