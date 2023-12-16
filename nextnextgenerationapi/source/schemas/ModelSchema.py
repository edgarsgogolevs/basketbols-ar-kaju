from marshmallow import Schema, fields, EXCLUDE


class ModelSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    profile_picture = fields.Url()
    picture_small = fields.Url()
    nominal_precision = fields.Float()
    
