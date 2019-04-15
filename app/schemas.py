from app import ma
from flask import current_app
from app.models import Team, Game, User, Vote

class TeamSchema(ma.ModelSchema):
    class Meta:
        model = Team

class GameSchema(ma.ModelSchema):
    class Meta:
        model = Game

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class VoteSchema(ma.ModelSchema):
    class Meta:
        model = Vote