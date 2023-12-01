from flask import Blueprint, jsonify, request
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from modules.predict import predict_games  # type: ignore
import modules.models as models
import modules.validate
import modules.db as db

from schemas.GamePredictionSchema import GamePredictionSchema # type: ignore

bp = Blueprint("predictions", __name__, url_prefix="/predictions")
lg = logging.getLogger("api.predictions")


@bp.route("/predict_game/<int:game_id>/<int:model_id>", methods=["GET"])
@marshal_with(GamePredictionSchema)
def predict_game():
    # TODO: implement
    return "Game prediction"


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
#
#
# @bp.route("/test", methods=["GET"])
# def test():
#     lg.info("Testing connection to database")
#     conn = db.get_conn()
#     cursor = conn.cursor()
#     cursor.execute("SELECT @@version;")
#     row = cursor.fetchone()
#     if row is None:
#         return jsonify("No data"), 500
#     return jsonify(row[0]), 200


