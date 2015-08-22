"""
Scrape all matches for the next five days from live-footballontv.com
"""
import re
import requests
from bs4 import BeautifulSoup as bs
from app.models import Match, Team, Competition, Channel
from app import db
from datetime import datetime


def parse_page():
    """
    Parse the matches from the website
    """
    page = requests.get(
        'http://www.live-footballontv.com',
        headers={'User-Agent':
                 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})

    soup = bs(page.text)
    listings = soup.find('div', {'id': 'listings'})

    matches = {}
    prev_date = ''

    for row in listings.find_all('div', {'class': 'row-fluid'})[:-10]:
        is_date = row.find('div', {'class': 'matchdate'})

        if is_date:
            prev_date = is_date.get_text()
            matches[prev_date] = []
        else:
            # Get the temas thta are playing
            fixture = row.find('div', {'class':
                                       'matchfixture'}).get_text().split(' v ')
            fixture = [team.strip() for team in fixture]
            # Get the competition name
            competition = row.find('div', {'class': 'competition'}).get_text()
            # Get the match time
            kickofftime = row.find('div', {'class': 'kickofftime'}).get_text()
            channels = row.find('div', {'class':
                                        'channels'}).get_text().split(
                                                '\xa0/\xa0')
            match = {'fixture': fixture, 'competition': competition,
                     'kickofftime': kickofftime, 'channels': channels}
            matches[prev_date].append(match)

    return matches


def check_exist(table, namesearch):
    for element in table:
        if element.name == namesearch:
            return element


def parse_date(date, time):
    date = date.split()
    date[1] = re.sub('\D', '', date[1])
    date = ' '.join(date)
    try:
        return datetime.strptime('{} {}'.format(date, time),
                                 '%A %d %B %Y %H:%M')
    except ValueError:
        return False


def populate():
    """
    Populate database with matches
    """
    collection = []

    teams = []
    competitions = []
    channels = []

    all_fixtures = parse_page()

    teams.append(Team(name='TBC'))

    for day in all_fixtures:
        for match in all_fixtures[day]:
            # Check if team objects already exist
            if match['fixture'][0] == 'TBC':
                # If the teams are to be confirmed
                home_team, away_team = teams[0], teams[0]
            else:
                home_team = check_exist(teams, match['fixture'][0])
                away_team = check_exist(teams, match['fixture'][1])

                if not home_team:
                    home_team = Team(name=match['fixture'][0])
                    teams.append(home_team)
                if not away_team:
                    away_team = Team(name=match['fixture'][1])
                    teams.append(away_team)

            match_channels = []
            for channel_name in match['channels']:
                channel = check_exist(channels, channel_name)
                if not channel:
                    channel = Channel(name=channel_name)
                    channels.append(channel)
                match_channels.append(channel)

            competition = check_exist(competitions, match['competition'])

            if not competition:
                competition = Competition(name=match['competition'])
                competitions.append(competition)

            match_time = parse_date(day, match['kickofftime'])

            if match_time:
                date = match_time.date()
                kickoff = match_time.time()
                collection.append(
                    Match(home_team=home_team, away_team=away_team,
                          channels=match_channels, competition=competition,
                          time=kickoff, date=date)
                )

    db.session.add_all(collection)
    db.session.commit()
    return True
