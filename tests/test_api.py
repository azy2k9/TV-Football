import unittest
from flask import current_app
from flask.ext.restful import Api
from app import create_app, db, models, resources
from datetime import datetime, date


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def generate_match(self):
        home = models.Team(name='Manchester United')
        away = models.Team(name='Tottenham')
        competition = models.Competition(name='Premier League')
        channel = models.Channel(name='BT Sport')
        time = datetime.utcnow().time()
        match_date = date.today()

        return models.Match(
                home_team=home, away_team=away, channels=[channel],
                time=time, date=match_date, competition=competition
                )

    def test_404(self):
        response = self.client.get('/wrong/url')
        self.assertTrue(response.status_code == 404)

    def test_matches_endpoint(self):
        db.session.add(self.generate_match())
        db.session.commit()
        response = self.client.get(Api.url_for(self.app.api, resource=resources.MatchListResource))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(b'data' in response.data)
