from flask import Blueprint, jsonify
import logging
from flask_apispec import marshal_with, use_kwargs  # type: ignore

from schemas.TeamSchema import TeamSchema


lg = logging.getLogger("api.teams")
bp = Blueprint("teams", __name__, url_prefix="/teams")


@bp.route("/all", methods=["GET"])
@marshal_with(TeamSchema(many=True))
def get_all_teams():
    # TODO: implement
    return jsonify({"teams": "all"})


@bp.route("/<int:team_id>", methods=["GET"])
@marshal_with(TeamSchema)
def get_team(team_id: int):
    # TODO: implement
    return jsonify({"team": team_id})

