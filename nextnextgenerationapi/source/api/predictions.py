from flask import Blueprint, jsonify, request
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from modules.predict import predict_game_by_game_id_model_id # type: ignore
import modules.validate as validate
from modules.db import Db

from schemas.GamePredictionSchema import GamePredictionSchema, GamePredictionRequestSchema # type: ignore

bp = Blueprint("predictions", __name__, url_prefix="/predictions")
lg = logging.getLogger("api.predictions")
db = Db()


@bp.route("/predict_game/<int:game_id>/<int:model_id>", methods=["GET"])
@marshal_with(GamePredictionSchema, code=200)
@validate.schema(GamePredictionRequestSchema)
def predict_game(game_id: int, model_id: int):
    """
    Predict game outcome by game id.
    """
    prediction = predict_game_by_game_id_model_id(game_id, model_id)
    if not prediction:
        return {"error": "Game not found"}, 404
    return prediction


@bp.route("/predict_games/<int:model_id>", methods=["GET"])
@marshal_with(GamePredictionSchema(many=True), code=200)
def get_models_predicted_games(model_id: int):
    """
    List of predicted games by model.
    """
    data = db.select("SELECT * FROM basketball.game_predictions WHERE model_id = ?", (model_id,))
    if not data:
        return {"error": "Not found"}, 404
    return data
