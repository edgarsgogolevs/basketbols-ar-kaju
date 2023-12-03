from flask import Blueprint, jsonify
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from schemas.GameSchema import GameSchema
from schemas.ResponseSchemas import SuccessSchema


lg = logging.getLogger("api.games")
bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("/", methods=["POST"])
@use_kwargs(GameSchema(only=["team_home_id", "team_away_id", "game_date"]))
@marshal_with(SuccessSchema, code=201)
def add_game():
    """
    In case game not in db.
    Look up suggested game on nba website or api
    and insert it to db.
    """
    responses = {
        201: {"Description" : "Created", "model": SuccessSchema}
    }
    # TODO: Implement
    return {"message": "ok"}, 201


@bp.route("/upcoming/<int:count>", methods=["GET"])
@marshal_with(GameSchema(many=True))
def upcoming_games(count: int):
    # TODO: Implement
    return f"{count} upcoming games"


@bp.route("/head_to_head/<int:team1>/<int:team2>")
@marshal_with(GameSchema)
def get_head_to_head_games(team1: int, team2: int):
    # TODO: Implement
    return f"matches of team {team1} and {team2}"
