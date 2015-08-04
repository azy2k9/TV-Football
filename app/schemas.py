"""
Schemas
"""
from marshmallow import Schema, fields


class TeamSchema(Schema):
    """
    doc
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()


class MatchSchema(Schema):
    """
    Match Schema
    """
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    time = fields.Time(dump_only=True)
    home_team = fields.Nested(TeamSchema)
    away_team = fields.Nested(TeamSchema)
    competition = fields.Nested('CompetitionSchema', only=['id', 'name'])
    channels = fields.Nested('ChannelSchema', only=['id', 'name'], many=True)


class CompetitionSchema(Schema):
    """
    Competition Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
    matches = fields.Nested(MatchSchema)


class ChannelSchema(Schema):
    """
    Channel Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
    matches = fields.Nested(MatchSchema)
