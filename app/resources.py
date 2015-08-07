"""
Resources
"""
import datetime
from flask import jsonify
from flask.ext.restful import Resource, reqparse
from . import models, schemas


class TeamResource(Resource):
    """
    Team Resource
    """
    team_schema = schemas.TeamSchema()

    def get(self, id):
        team = models.Team.query.get(id)
        if team:
            result = self.team_schema.dump(team)
            return jsonify(result.data)
        else:
            return jsonify(result='Not Found')


class MatchResource(Resource):
    """
    Match Resource
    """
    match_schema = schemas.MatchSchema()

    def get(self, id):
        match = models.Match.query.get(id)
        if match:
            result = self.match_schema.dump(match)
            return jsonify(result.data)
        else:
            return jsonify(result='Not Found')


class MatchListResource(Resource):
    """
    Match List Resource

    TODO: write some tests here
    """
    match_list_schema = schemas.MatchSchema(many=True)

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('date')

    def get(self):
        args = self.parser.parse_args()
        if not args['date']:
            matches = models.Match.query.all()
            result = self.match_list_schema.dump(matches)
            return jsonify(data=result.data)
        else:
            try:
                parsed_date = tuple([int(i) for i in args['date'].split('-')])
                date = datetime.date(*parsed_date)
            except ValueError:
                return jsonify(result='Invalid date format')
            matches = models.Match.query.filter(
                    models.Match.date == date
                    ).order_by(models.Match.time).all()
            result = self.match_list_schema.dump(matches)
            return jsonify(data=result.data)


class TeamMatchListResource(Resource):
    """
    doc
    """

    def get(self, id):
        team = models.Team.query.get(id)
        result = MatchListResource.match_list_schema.dump(team.matches)
        return jsonify(data=result.data)
