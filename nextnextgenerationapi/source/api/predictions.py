from flask import Blueprint, jsonify, request
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from modules.predict import predict_game_by_game_id_model_id # type: ignore
import modules.validate as validate

from schemas.GamePredictionSchema import GamePredictionSchema, GamePredictionRequestSchema # type: ignore

bp = Blueprint("predictions", __name__, url_prefix="/predictions")
lg = logging.getLogger("api.predictions")


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
@marshal_with(GamePredictionSchema(many=True))
def get_models_predicted_games():
    """
    List of predicted games by model.
    """
    # TODO: Implement
    return "List of predicted games"


# @bp.route("/<string:model>", methods=["GET"])
# @modules.validate.schema(PredictGameRequestSchema)
# def predict_game_outcome(model: str):
#     lg.info("Predicting game outcome with logistic regression")
#     data = request.parsed["PredictGameRequest"] # type: ignore
#     model_obj = models.MODEL_MAPPING[model]
#     team_home = data["team_home"]
#     team_away = data["team_away"]
#     predict_home_win, predict_winning_probability = predict_games(
#         model_obj, team_home, team_away
#     )
#     ret = {
#         "team_home": team_home,
#         "team_away": team_away,
#         "predict_home_win": int(predict_home_win),
#         "predict_winning_probability": float(predict_winning_probability),
#     }
#     return jsonify(ret), 200
