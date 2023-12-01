from marshmallow import Schema, fields, EXCLUDE

class SuccessSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    success = fields.Bool()
    message = fields.Str()
    data = fields.Dict()
