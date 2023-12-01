from flask import Blueprint, jsonify
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from schemas.ModelSchema import ModelSchema  # type: ignore
from schemas.GamePredictionSchema import ModelStatsSchema


lg = logging.getLogger("api.prediction_models")
bp = Blueprint("models", __name__, url_prefix="/models")


@bp.route("/all", methods=["GET"])
@marshal_with(ModelSchema(many=True))
def get_all_models():
    # TODO: Implement
    return jsonify({"models": "all"})


@bp.route("/<int:id>", methods=["GET"])
@marshal_with(ModelSchema)
def get_model(model_id: int):
    # TODO: Implement
    return jsonify({"model": model_id})


@bp.route("/<int:model_id>/stats", methods=["GET"])
@marshal_with(ModelStatsSchema)
def get_model_stats(model_id: int):
    # TODO: Implement
    return "stats"
