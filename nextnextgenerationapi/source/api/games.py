from flask import Blueprint, jsonify
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from modules.db import Db

from schemas.GameSchema import GameSchema
from schemas.ResponseSchemas import SuccessSchema


lg = logging.getLogger("api.games")
bp = Blueprint("games", __name__, url_prefix="/games")
db = Db()

GAME_FIELDS = "team_home as team_home_id, team_away as team_away_id, home_won, score_home, score_away, game_date, id"

@bp.route("/", methods=["POST"])
@use_kwargs(GameSchema(only=["team_home_id", "team_away_id", "game_date"]))
@marshal_with(SuccessSchema, code=201)
def add_game():
    """
    In case game not in db.
    Look up suggested game on nba website or api
    and insert it to db.
    """
    responses = {201: {"Description": "Created", "model": SuccessSchema}}
    # TODO: Implement
    return {"message": "ok"}, 201


@bp.route("/upcoming/<int:count>", methods=["GET"])
@marshal_with(GameSchema(many=True, exclude=["team_home", "team_away"]))
def upcoming_games(count: int):
    if count > 1000:
        lg.warning("Count > 1000, setting to 1000")
        count = 1000
    data = db.select(
        f"SET ROWCOUNT ?;\
        SELECT id, team_home as team_home_id, team_away as team_away_id, game_date\
        FROM basketball.games where game_date > GETDATE() ORDER BY game_date ASC",
        (count,),
    )
    if not data:
        return {"error": "Not found"}, 404
    return data


@bp.route("/recent/<int:count>", methods=["GET"])
@marshal_with(GameSchema(many=True, exclude=["team_home", "team_away"]))
def recent_games(count: int):
    if count > 1000:
        lg.warning("Count > 1000, setting to 1000")
        count = 1000
    data = db.select(
        f"SET ROWCOUNT ?; SELECT {GAME_FIELDS} FROM basketball.games where game_date < GETDATE() and score_home is not null ORDER BY game_date DESC",
        (count,),
    )
    if not data:
        return {"error": "Not found"}, 404
    return data


@bp.route("/head_to_head/<int:team1>/<int:team2>")
@marshal_with(GameSchema)
def get_head_to_head_games(team1: int, team2: int):
    data = db.select(
        f"SET ROWCOUNT 100; SELECT {GAME_FIELDS} \
        FROM basketball.games WHERE team_home=? AND team_away=? OR team_home=? AND team_away=? ORDER BY game_date",
        (team1, team2, team2, team1),
    )
    if not data:
        return {"error": "Not found"}, 404
    return data
