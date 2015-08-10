"""
Resources
"""
from operator import attrgetter
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
        self.parser.add_argument('start')
        self.parser.add_argument('end')

    def date_parser(self, date_string):
        try:
            parsed_date = tuple([int(i) for i in date_string.split('-')])
            parsed_date = datetime.date(*parsed_date)
        except (ValueError, TypeError):
            return False

        return parsed_date

    def get(self):
        args = self.parser.parse_args()
        if args['date']:
            date = self.date_parser(args['date'])
            if not date:
                return jsonify(result='Invalid date format')

            # Find matches that are on this given day
            matches = models.Match.query.filter(
                    models.Match.date == date
                    ).order_by(models.Match.time).all()
            result = self.match_list_schema.dump(matches)
            return jsonify(data=result.data)

        elif args['start'] and args['end']:
            start = self.date_parser(args['start'])
            end = self.date_parser(args['end'])
            if not (start or end):
                return jsonify(result='Invalid date format')

            matches = models.Match.query.filter(
                    models.Match.date >= start,
                    models.Match.date <= end
                    ).all()

            # Group by date
            grouped = {match.date.isoformat(): [] for match in matches}
            for match in matches:
                date = match.date.isoformat()
                grouped[date].append(
                        match
                        )

            for k in grouped:
                # Sort by time
                grouped[k] = sorted(grouped[k], key=attrgetter('time'))
            # Serialise
                grouped[k] = self.match_list_schema.dump(grouped[k]).data
            return jsonify(grouped)

        else:
            matches = models.Match.query.all()
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
