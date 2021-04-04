from flask import Flask, request
from flask_cors import CORS

from resources.conf import config_by_name
from resources.util import CustomJSONEncoder
from database.database_api import init_db
# from sample_download.background_job import BackgroundJob

from resources.routes import api
from resources.errorhandlers import api_errors, not_found_handler


def _handle_api_error_404(error):
    if request.path.startswith('/api/v0.1'):
        return not_found_handler(error)
    else:
        return error


def create_app(config_name: str) -> Flask:
    # Initialize resources
    app = Flask("plancton_visualizer_server")
    # Add CORS
    CORS(app)
    # Add configuration
    app.config.from_object(config_by_name[config_name])
    init_db(app.config["MONGODB"]["URL"], app.config["MONGODB"]["DATABASE"])
    app.json_encoder = CustomJSONEncoder
    # Start background job
    # resources.config["BACKGROUND_JOB"] = BackgroundJob(30)

    # Register the routes and error handlers of the API
    app.register_blueprint(api, url_prefix="/api/v0.1")
    app.register_blueprint(api_errors, url_prefix="/api/v0.1")
    # Register the 404 error handler manually, since it wouldn't be called otherwise
    app.register_error_handler(404, _handle_api_error_404)

    return app
