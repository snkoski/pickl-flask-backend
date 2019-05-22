import os
import base64
from datetime import datetime, timedelta
from app import db, guard, login
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(15), unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')
    total_votes = db.Column(db.Integer, default=0)
    votes = db.relationship('Vote', backref='voter')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    def set_password(self, password):
        self.password = guard.encrypt_password(password)

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'phone', 'roles']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
        
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     total_votes = db.Column(db.Integer, default=0)
#     votes = db.relationship('Vote', backref='voter')
#     token = db.Column(db.String(32), index=True, unique=True)
#     token_expiration = db.Column(db.DateTime)

#     def __repr__(self):
#         return f'<User {self.username}>'

#     def __str__(self):
#         return f'{self.username}'

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def get_token(self, expires_in=3600):
#         now = datetime.utcnow()
#         if self.token and self.token_expiration > now + timedelta(seconds=60):
#             return self.token
#         self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
#         self.token_expiration = now + timedelta(seconds=expires_in)
#         db.session.add(self)
#         return self.token

#     def revoke_token(self):
#         self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

#     @staticmethod
#     def check_token(token):
#         user = User.query.filter_by(token=token).first()
#         if user is None or user.token_expiration < datetime.utcnow():
#             return None
#         return user

#     def add_vote(self):
#         self.total_votes += 1

#     def remove_vote(self):
#         if self.total_votes > 0:
#             self.total_votes -= 1

#     def vote_for_team(self, game, teamy):
#         new_vote = Vote(voter=self, game=game, team=teamy)
#         teamy.add_vote()
#         print(teamy.total_votes)

#         db.session.add(new_vote)
#         db.session.commit()
#         print(new_vote.voter)

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

    def __repr__(self):
        return f'<Team {self.name}>'

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
    original_date = db.Column(db.Date, default=None)
    original_time = db.Column(db.Time, default=None)
    delayed_or_postponed_reason = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Time)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    votes = db.relationship('Vote', backref='game')

    def __repr__(self):
        return f'<Game {self.id}>'

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} @ {self.location} on {self.date}'

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return f'<Vote {self.id}>'

    def __str__(self):
        user = User.query.get(self.user_id)
        game = Game.query.get(self.game_id)
        team = Team.query.get(self.team_id)
        
        return f'In the game between the {game.home_team.name} and {game.away_team.name}, {user.username} thinks the {team.name} will win'

    @classmethod
    def place_vote(cls, user, game, team):
        vote = Vote(voter=user, game=game, team=team)
        user.add_vote()
        team.add_vote()
        db.session.add(vote)
        db.session.commit()
