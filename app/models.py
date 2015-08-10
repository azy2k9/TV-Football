from . import db


match_channels = db.Table(
    'match_channels',
    db.Column('match_id', db.Integer, db.ForeignKey('matches.id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'))
    )


class Team(db.Model):
    """
    Team Class
    """
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    @property
    def matches(self):
        return self.home_matches + self.away_matches

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Match(db.Model):
    """
    Match Class
    """
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'))

    channels = db.relationship('Channel', secondary=match_channels,
                               backref=db.backref('matches', lazy='dynamic'))
    home_team = db.relationship('Team', foreign_keys=home_team_id,
                                backref='home_matches')
                                # backref=db.backref('matches', lazy='dynamic'))
    away_team = db.relationship('Team', foreign_keys=away_team_id,
                                backref='away_matches')
                                # backref=db.backref('matches', lazy='dynamic'))

    def __repr__(self):
        return '<Match {} v {}>'.format(self.home_team.name,
                                        self.away_team.name)


class Competition(db.Model):
    """
    Competition Class
    """
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    matches = db.relationship('Match', backref='competition', lazy='dynamic')

    def __repr__(self):
        return '<Competition {}>'.format(self.name)


class Channel(db.Model):
    """
    Channels Class
    """
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)


    def __repr__(self):
        return '<Channel {}>'.format(self.name)
