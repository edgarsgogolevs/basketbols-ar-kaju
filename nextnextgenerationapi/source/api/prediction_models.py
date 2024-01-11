from flask import Blueprint, jsonify
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from modules.db import Db
from modules.models import calculate_model_stats, create_history

from schemas.GamePredictionSchema import ModelSchema, ModelHistorySchema # type: ignore

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
    for model in data:
        model_id = model["id"]
        stats = calculate_model_stats(model_id)
        model.update(stats)
    return data


@bp.route("/<int:model_id>", methods=["GET"])
@marshal_with(ModelSchema, code=200)
def get_model(model_id: int):
    data = db.select(f"SELECT * FROM {DEFAULT_TABLE} WHERE id=?", (model_id, ))
    if not data:
        return {"error": "Not found"}, 404
    stats = calculate_model_stats(model_id)
    data[0].update(stats)
    return data[0]


@bp.route("/<int:model_id>/history", methods=["GET"])
@marshal_with(ModelHistorySchema, code=200)
def get_model_stats(model_id: int):
    history = create_history(model_id)
    ret = {
        "model_id": model_id,
        "history": history
    }
    return ret
