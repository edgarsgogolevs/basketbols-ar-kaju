from marshmallow import Schema, fields, EXCLUDE, validate
from schemas.GameSchema import GameSchema

from modules.db import Db

db = Db()

model_ids = [
    model["id"]
    for model in db.select("SELECT id FROM basketball.prediction_models")
]


class ModelSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    profile_picture = fields.Url()
    picture_small = fields.Url()
    nominal_precision = fields.Float()
    last_ten_accuracy = fields.Float()
    all_time_accuracy = fields.Float()


class GamePredictionSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    game_id = fields.Int()
    model_id = fields.Int()
    game = fields.Nested(GameSchema(exclude=["team_home", "team_away"]))
    model = fields.Nested(ModelSchema)
    home_wins = fields.Bool()
    home_winning_proba = fields.Float()
    prediction_correct = fields.Bool()
    updated_at = fields.DateTime()


class ModelHistorySchema(Schema):

    class Meta:
        unknown = EXCLUDE
    model_id = fields.Int(required=True)
    history = fields.List(
        fields.Nested(GamePredictionSchema(exclude=["model"])), required=True)


class GamePredictionRequestSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    model_id = fields.Int(validate=validate.OneOf(model_ids), required=True)
    game_id = fields.Int(required=True)
