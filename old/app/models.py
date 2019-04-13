from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@logn.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    votes = db.relationship('Vote', backref='voter', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(Self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, passsword)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    city = db.Column(db.String(64), index=True)
    abbreviation = db.Column(db.String(3), index=True, unique=True)
    votes = db.relationship('Vote', backref='team', lazy='dynamic')
    games = db.relationship('Game', primaryjoin='or_(Team.id==Game.home_team, Team.id==Game.away_team)', lazy='dynamic')

    def __repr__(self):
        return '<Team {}>'.format(self.name)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    date = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(64))
    schedule_status = db.Column(db.String(64))
    original_date = db.Column(db.DateTime)
    original_time = db.Column(db.DateTime)
    delayed_or_postponed_reason = db.Column(db.String(64))
    votes = db.relationship('Vote', backref='game', lazy='dynamic')

    def __repr__(self):
        return '<Game {} vs {}>'.format(self.home_team, self.away_team)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Vote by {} for {} during {}>'.format(self.user_id, self.team_id, self.game_id)
