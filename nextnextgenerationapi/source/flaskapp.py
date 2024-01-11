import logging
from os import environ

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s [%(name)s]: %(message)s")

root_logger = logging.getLogger()
LOGLEVEL = environ.get("LOGLEVEL")
if not LOGLEVEL or not isinstance(LOGLEVEL, str):
    raise ValueError("LOGLEVEL environment variable not set")
logging.basicConfig(level=LOGLEVEL,
                    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s")
root_logger.info("Logger initialized")

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

CORS(app)

# Register blueprints
from api.predictions import bp as predictions_bp
from api.games import bp as games_bp
from api.teams import bp as teams_bp
from api.prediction_models import bp as prediction_models_bp

app.register_blueprint(predictions_bp)
app.register_blueprint(games_bp)
app.register_blueprint(teams_bp)
app.register_blueprint(prediction_models_bp)

from flask_apispec.extension import FlaskApiSpec  # type: ignore
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from apispec import APISpec

app.config.update({
    "APISPEC_SPEC":
    APISpec(
        title="basketball-ar-kaju",
        version="v1",
        openapi_version="2.0",
        plugins=[MarshmallowPlugin()],
    ),
    "APISPEC_SWAGGER_URL":
    "/swagger/",
    "APISPEC_SWAGGER_UI_URL":
    "/swagger-ui/",
})

docs = FlaskApiSpec(app)
docs.register_existing_resources()


# 404 error handling
@app.errorhandler(404)
def pageNotFound(error):
    return {"error": "Not found"}, 404


@app.after_request
def after_request_func(response):
    root_logger.info(f"Response {response.status_code}: {response.get_json()}")
    return response


@app.errorhandler(500)
def server_error(e):
    root_logger.critical(str(e), exc_info=True)
    return {"error": "Processing error"}, 500


# hello world message
@app.route("/", methods=["GET"])
def hello_word():
    return {"message": "Welcome to BasketBallArKaju API version 7.3"}


# devel mode run
if __name__ == "__main__":
    # run debug app
    PORT = environ.get("PORT")
    if not PORT or not isinstance(PORT, str):
        raise ValueError("PORT environment variable not set")
    app.run(debug=True, port=int(PORT))
