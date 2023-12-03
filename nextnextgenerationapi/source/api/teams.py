from flask import Blueprint, jsonify
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from schemas.TeamSchema import TeamSchema
from modules.db import Db

TEAMS_TABLE = "basketball.teams"

lg = logging.getLogger("api.teams")
bp = Blueprint("teams", __name__, url_prefix="/teams")
db = Db()

@bp.route("/all", methods=["GET"])
@marshal_with(TeamSchema(many=True))
def get_all_teams():
    data = db.select(f"SELECT * FROM {TEAMS_TABLE}")
    if not data:
        return {"error": "Not found"}, 404
    ret = TeamSchema(many=True).dump(data)
    return jsonify(ret)


@bp.route("/<int:team_id>", methods=["GET"])
@marshal_with(TeamSchema)
def get_team(team_id: int):
    # TODO: implement
    return jsonify({"team": team_id})

