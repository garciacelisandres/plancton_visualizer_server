import logging
import os
from os import environ

from flask import Flask, request
from flask_cors import CORS
from flask_talisman import Talisman
from flask_seasurf import SeaSurf

from database.database_api import init_db
from resources.conf import config_by_name
from resources.errorhandlers import not_found_handler
from resources.routes import api
from resources.util import CustomJSONEncoder

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def _handle_api_error_404(error):
    if request.path.startswith('/api/v0.1'):
        return not_found_handler(error)
    else:
        return error


def create_app(config_name: str) -> Flask:
    # Initialize resources
    app = Flask(__name__)
    # Add CORS and security middlewares
    CORS(app)
    if config_name == "prod":
        csp = {
            "report-uri": "\'none\'",
            "default-src": "\'self\'",
            "script-src": "\'none\'",
            "style-src": "\'none\'",
            "worker-src": "\'none\'",
            "object-src": "\'none\'",
            "base-uri": "\'self\'",
            "frame-ancestors": "\'none\'",
            "form-action": "\'none\'",
            "require-trusted-types-for": "\'script\'",
        }
        Talisman(app, content_security_policy=csp)  # adds CSP and another security preventions
        # SeaSurf(app)  # prevents CSRF
    # Add configuration
    app.config.from_object(config_by_name[config_name])
    init_db(app.config["MONGODB"]["URL"], app.config["MONGODB"]["DATABASE"])
    app.json_encoder = CustomJSONEncoder

    # Register the routes and error handlers of the API
    app.register_blueprint(api, url_prefix="/api/v0.1")
    # Register the 404 error handler manually, since it wouldn't be called otherwise
    app.register_error_handler(404, _handle_api_error_404)

    # Execute background sample download job if specified
    exec_back_job = bool(int(environ.get('BACKGROUND_JOB')))
    if exec_back_job:
        from sample_download.background_job import BackgroundJob
        BackgroundJob(1200, True)

    # Configure the logging for the API
    logging.basicConfig(
        format="[%(asctime)s] API - %(levelname)s: %(message)s",
        filemode="a",
        filename=f"{environ.get('CONTEXT')}api.log",
        level=logging.INFO
    )

    return app
