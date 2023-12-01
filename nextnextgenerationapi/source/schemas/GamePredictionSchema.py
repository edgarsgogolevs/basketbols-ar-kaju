from marshmallow import Schema, fields, EXCLUDE
from schemas.ModelSchema import ModelSchema
from schemas.GameSchema import GameSchema


class GamePredictionSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    game_id = fields.Int()
    model_id = fields.Int()
    game = fields.Nested(GameSchema)
    model = fields.Nested(ModelSchema)
    home_wins = fields.Bool()
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
