from flask import Blueprint, jsonify
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from modules.db import Db
from modules.models import calculate_model_stats

from schemas.ModelSchema import ModelSchema  # type: ignore
from schemas.GamePredictionSchema import ModelStatsSchema

lg = logging.getLogger("api.prediction_models")
bp = Blueprint("models", __name__, url_prefix="/models")
db = Db()

DEFAULT_TABLE = "basketball.prediction_models"


@bp.route("/all", methods=["GET"])
@marshal_with(ModelSchema(many=True), code=200)
def get_all_models():
    data = db.select(f"SELECT * FROM {DEFAULT_TABLE}")
    if not data:
        return {"error": "Not found"}, 404
    return data


@bp.route("/<int:model_id>", methods=["GET"])
@marshal_with(ModelSchema, code=200)
def get_model(model_id: int):
    data = db.select(f"SELECT * FROM {DEFAULT_TABLE} WHERE id=?", (model_id, ))
    if not data:
        return {"error": "Not found"}, 404
    return data[0]


@bp.route("/<int:model_id>/stats", methods=["GET"])
@marshal_with(ModelStatsSchema, code=200)
def get_model_stats(model_id: int):
    return calculate_model_stats(model_id)
