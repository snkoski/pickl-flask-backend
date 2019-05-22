import datetime
from app import db, guard
from app.api import bp
from app.api.errors import bad_request
from flask import jsonify, url_for, abort, request
from app.models import Vote, Team, Game, User
from app.schemas import VoteSchema
from flask_praetorian import auth_required, roles_required, current_user

@bp.route('/votes/<int:id>', methods=['GET'])
@auth_required
def get_user_votes(id):
    
    print("User", current_user())
    user = User.query.get(id)
    votes = user.votes
    vote_schema = VoteSchema(many=True)
    output = vote_schema.dump(votes).data
    return jsonify({'votes' : output})

@bp.route('/votes/<int:id>/today', methods=['GET'])
@auth_required
def get_user_votes_today(id):
    if current_user().id != id:
        abort(403)
    # print("USer", current_user())
    today = str(datetime.date.today())
    user = User.query.get(id)
    votes = user.votes
    todays_games = Game.query.filter(Game.date == today).all()
    todays_votes = []

    for game in todays_games:
        for vote in votes:
            if vote.game_id == game.id:
                todays_votes.append(vote)

    vote_schema = VoteSchema(many=True)
    output = vote_schema.dump(todays_votes).data
    return jsonify({'votes' : output})

@bp.route('/votes', methods=['GET'])
def get_all_votes():
    votes = Vote.query.all()
    vote_schema = VoteSchema(many=True)
    output = vote_schema.dump(votes).data
    return jsonify({'votes': output})

@bp.route('/votes', methods=['POST'])
@auth_required
def add_vote():
    req = request.get_json(force=True)
    user_id = req.get('user_id', None)
    game_id = req.get('game_id', None)
    team_id = req.get('team_id', None)
    if current_user().id != user_id:
        abort(403)
    game = Game.query.get(game_id)
    if not game:
        return bad_request('Game not found')
    team = Team.query.get(team_id)
    if not team:
        return bad_request('Team not found')
    if game.home_team != team and game.away_team != team:
        return bad_request('Team not playing in game')
    vote = Vote.query.filter_by(user_id=user_id, game_id=game_id).first()
    if not vote:
        vote = Vote(user_id=user_id, game_id=game_id, team_id=team_id)
        db.session.add(vote)
        db.session.commit()
    elif vote.team != team:
        vote.team = team
        db.session.commit()
    vote_schema = VoteSchema()
    output = vote_schema.dump(vote).data
    return jsonify({'vote': output})
