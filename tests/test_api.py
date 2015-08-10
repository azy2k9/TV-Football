import unittest
from flask import current_app
from app import create_app, db, models, resources
from datetime import datetime, date, timedelta


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
        match = self.generate_match()
        db.session.add(match)
        db.session.commit()

        response = self.client.get('/api/matches')
        self.assertTrue(response.status_code == 200)
        self.assertIn(b'data', response.data)

        response = self.client.get('/api/match/1')
        self.assertTrue(response.status_code == 200)
        self.assertIn(b'Manchester United', response.data)

        response = self.client.get('/api/matches?date=fakedate')
        self.assertIn(b'Invalid date format', response.data)

        response = self.client.get('/api/matches',
                data={
                    'date': date.today().isoformat()
                    }
                )
        self.assertIn(b'Manchester United', response.data)

        response = self.client.get(
                '/api/matches',
                data={
                    'start': 'fake',
                    'end': 'fake'
                    }
                )
        self.assertIn(b'Invalid date format', response.data)

        # End date for range test
        response = self.client.get(
                '/api/matches',
                data={
                    'start': date.today().isoformat(),
                    'end': date.today().isoformat()
                    }
                )
        self.assertTrue(response.status_code == 200)
        self.assertIn(b'Manchester United', response.data)
        self.assertIn(b'Tottenham', response.data)

        response = self.client.get(
                '/api/match/5'
                )
        self.assertIn(b'Not Found', response.data)


    def test_team_endpoint(self):
        match = self.generate_match()
        db.session.add(match)
        db.session.commit()
        response = self.client.get('/api/team/1')
        self.assertIn(b'Manchester United', response.data)
        self.assertTrue(response.status_code == 200)

        response = self.client.get('/api/team/2')
        self.assertIn(b'Tottenham', response.data)
        self.assertTrue(response.status_code == 200)

        response = self.client.get('/api/team/3')
        self.assertIn(b'Not Found', response.data)

        response = self.client.get(
                '/api/team/1/matches'
                )
        self.assertTrue(response.status_code == 200)
