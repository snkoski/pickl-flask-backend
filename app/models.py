from app import db
from flask import current_app

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
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    votes = db.relationship('Vote', backref='game')

    def __repr__(self):
        return f'<Game {self.id}>'

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} @ {self.location} on {self.date}'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    total_votes = db.Column(db.Integer, default=0)
    votes = db.relationship('Vote', backref='voter')

    def __repr__(self):
        return f'<User {self.username}>'

    def __str__(self):
        return f'{self.username}'

    def add_vote(self):
        self.total_votes += 1

    def remove_vote(self):
        if self.total_votes > 0:
            self.total_votes -= 1

    def vote_for_team(self, game, teamy):
        new_vote = Vote(voter=self, game=game, team=teamy)
        teamy.add_vote()
        print(teamy.total_votes)

        db.session.add(new_vote)
        db.session.commit()
        print(new_vote.voter)

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
