from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    city = db.Column(db.String(50))
    abbreviation = db.Column(db.String(3), unique=True)
    logo = db.Column(db.String(255), unique=True)
    total_votes = db.Column(db.Integer, default=0)
    home_games = db.relationship('Game', backref='home_team', primaryjoin='and_(Team.id==Game.home_team_id, )')
    away_games = db.relationship('Game', backref='away_team', primaryjoin='and_(Team.id==Game.away_team_id, )')
    votes = db.relationship('Vote', backref='team')

    def __str__(self):
        return f'{self.city} {self.name}'

    def add_vote(self):
        self.total_votes += 1

    def remove_vote(self):
        if self.total_votes > 0:
            self.total_votes -= 1

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_status = db.Column(db.String(50))
    delayed_or_postponed_reason = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    votes = db.relationship('Vote', backref='game')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    votes = db.relationship('Vote', backref='voter')

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
