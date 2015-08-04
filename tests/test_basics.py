import unittest
from flask import current_app
from scrape.scrape import populate
from app import create_app, db, models
import datetime


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_populate_db(self):
        self.assertTrue(populate())

    def test_all_matches(self):
        test_matches = []

        team1 = models.Team(name='Loserpool')
        team2 = models.Team(name='Southampton')
        team3 = models.Team(name='Chelsea')

        channel = models.Channel(name='BBC')
        competition = models.Competition(name='Premier League')

        test_matches.append(
                models.Match(
                    home_team=team1, away_team=team2,
                    channels=[channel], competition=competition,
                    time=datetime.datetime.utcnow().time(),
                    date=datetime.date.today()
                    )
                )

        test_matches.append(
                models.Match(
                    home_team=team2, away_team=team3,
                    channels=[channel], competition=competition,
                    time=datetime.datetime.utcnow().time(),
                    date=datetime.date.today()
                    )
                )

        test_matches.append(
                models.Match(
                    home_team=team2, away_team=team1,
                    channels=[channel], competition=competition,
                    time=datetime.datetime.utcnow().time(),
                    date=datetime.date.today()
                    )
                )

        db.session.add_all(test_matches)
        db.session.commit()
        self.assertTrue(team3.matches)
        self.assertTrue(team1.matches)
        self.assertEqual(len(team2.home_matches), 2)
        self.assertEqual(len(team2.away_matches), 1)
        self.assertEqual(len(team2.matches), 3)
