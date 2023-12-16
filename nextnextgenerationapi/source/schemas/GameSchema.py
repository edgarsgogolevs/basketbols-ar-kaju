from marshmallow import Schema, fields, EXCLUDE
from schemas.TeamSchema import TeamSchema


class GameSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    team_home = fields.Nested(TeamSchema)
    team_home_id = fields.Int()
    team_away = fields.Nested(TeamSchema)
    team_away_id = fields.Int()
    game_date = fields.Date(required=True)
    home_won = fields.Bool(allow_none=True)
    score_home = fields.Int()
    score_away = fields.Int()
