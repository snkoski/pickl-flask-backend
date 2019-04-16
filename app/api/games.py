from app.api import bp
from flask import jsonify, request
from app.models import Game, Team
from app.schemas import GameSchema
from app import db, helper

@bp.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    one_game = Game.query.get(id)
    game_schema = GameSchema()
    output = game_schema.dump(one_game).data
    return jsonify({'game': output})

@bp.route('/games', methods=['GET'])
def get_games():
    all_games = Game.query.all()
    game_schema = GameSchema(many=True)
    output = game_schema.dump(all_games).data
    return jsonify({'game': output})

@bp.route('/games', methods=['POST'])
def create_games():
    data = request.get_json(force=True)
    print(data)
    if data['originalDate'] != None:
        originalDate = helper.format_date(data['originalDate'])
    else:
        originalDate = None

    if data['originalTime'] != None:
        originalTime = helper.format_time(data['originalTime'])
    else:
        originalTime = None

    # if day['delayedOrPostponedReason'] != None:
    #     reason = 

    new_game = Game(schedule_status=data['scheduleStatus'],
             original_date=originalDate,
             original_time=originalTime,
             delayed_or_postponed_reason=data['delayedOrPostponedReason'],
             date=helper.format_date(data['date']), 
             time=helper.format_time(data['time']), 
             away_team_id = Team.query.filter_by(name=data['awayTeam']['Name']).first().id, 
             home_team_id = Team.query.filter_by(name=data['homeTeam']['Name']).first().id, 
             location=data['location'])
    db.session.add(new_game)
    db.session.commit()
    return 'hi'

@bp.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    pass
