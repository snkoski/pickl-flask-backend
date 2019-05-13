from app.api import bp
from flask import jsonify, request, redirect
from app.models import Game, Team
from app.schemas import GameSchema
from app import db, helper
import datetime
from twilio.twiml.messaging_response import MessagingResponse

@bp.route('/sms', methods=['GET', 'POST'])
def sms_dynamic():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")

    return str(resp)
    # return str("hey")

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

@bp.route('/games/today', methods=['GET'])
def get_todays_games():
    today = str(datetime.date.today())
    todays_games = Game.query.filter(Game.date == today).all()
    game_schema = GameSchema(many=True)
    output = game_schema.dump(todays_games).data
    return jsonify({'game': output})

@bp.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    pass

@bp.route('/test', methods=['GET', 'POST'])
def test():
    body = request.values.get('Body', None)
    resp = MessagingResponse()
    if body.lower() == 'mlb':
        today = str(datetime.date.today())
        todays_games = Game.query.filter(Game.date == today).all()
        teams = []
        for game in todays_games:
            time = game.time
            time = time.strftime("%-I:%M %p")
            string = f'{game.away_team.name} @ {game.home_team.name} {time}'
            teams.append(string)
        game_list = ',\n'.join(teams)
        print(game_list)
        resp.message(game_list)
    else:
        resp.message("I only know baseball games right now")
    return str(resp)
    # return jsonify({'test': 'worked'})