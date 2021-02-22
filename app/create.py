from flask import Flask
from flask_cors import CORS

from app.conf import config_by_name
from app.util import CustomJSONEncoder
from database.database_api import init_db
# from sample_download.background_job import BackgroundJob


def create_app(config_name: str) -> Flask:
    # Initialize app
    app = Flask(__name__)
    # Add CORS
    CORS(app)
    # Add configuration
    app.config.from_object(config_by_name[config_name])
    app.config["DB_CONNECTION"] = init_db(app.config["MONGODB"]["URL"], app.config["MONGODB"]["DATABASE"])
    app.json_encoder = CustomJSONEncoder
    # Start background job
    # app.config["BACKGROUND_JOB"] = BackgroundJob(30)

    return app
