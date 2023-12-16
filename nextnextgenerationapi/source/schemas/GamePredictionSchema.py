from marshmallow import Schema, fields, EXCLUDE, validate
from schemas.ModelSchema import ModelSchema
from schemas.GameSchema import GameSchema

from modules.db import Db

db = Db()

model_ids = [model["id"] for model in db.select("SELECT id FROM basketball.prediction_models")]

class GamePredictionSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    game_id = fields.Int()
    model_id = fields.Int()
    game = fields.Nested(GameSchema)
    model = fields.Nested(ModelSchema)
    home_wins = fields.Bool()
    home_winning_proba = fields.Float()
    prediction_correct = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ModelStatsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nominal_accuracy = fields.Float()
    last_ten_accuracy = fields.Float()
    all_time_accuracy = fields.Float()
    prediction_history = fields.List(fields.Nested(GamePredictionSchema))

class GamePredictionRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    model_id = fields.Int(validate=validate.OneOf(model_ids), required=True)
    game_id = fields.Int(required=True)
