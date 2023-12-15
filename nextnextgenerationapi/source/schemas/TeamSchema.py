from marshmallow import Schema, fields, EXCLUDE


class TeamSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    abbr = fields.Str(required=True)
    conference = fields.Str()
    description = fields.Str()
    town = fields.Str()
    logo_url = fields.Url()
    nba_url = fields.Url()
