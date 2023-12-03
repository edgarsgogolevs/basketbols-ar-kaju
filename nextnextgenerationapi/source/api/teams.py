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
    data = db.select(f"SELECT * FROM {TEAMS_TABLE} WHERE id=?", (team_id,))
    if not data:
        return {"error": "Not found"}, 404
    return TeamSchema().dump(data[0])


@bp.route("/by_abbr/<string:abbr>", methods=["GET"])
@marshal_with(TeamSchema)
def get_team_by_abbr(abbr: str):
    abbr = abbr.upper()
    data = db.select(f"SELECT * FROM {TEAMS_TABLE} WHERE abbr=?", (abbr,))
    if not data:
        return {"error": "Not found"}, 404
    return TeamSchema().dump(data[0])
